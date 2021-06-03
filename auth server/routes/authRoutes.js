const express = require('express')
const mongoose = require('mongoose')
const jwt = require('jsonwebtoken')
const { jwtkey } = require('../keys')
const router = express.Router();
const User = mongoose.model('User');
const Recipe = mongoose.model('Recipe');
const crypto = require('crypto');
const bcrypt = require('bcryptjs');
const requireLogin = require('../middleware/requireToken');
const nodemailer = require('nodemailer');
const sendgridTransport = require('nodemailer-sendgrid-transport')
var randomString = require('random-string');
// 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 (AllergyAssist1 API key)

// const {SENDGRID_API,EMAIL} = require('../config/keys')

const transporter = nodemailer.createTransport(sendgridTransport({
    auth: {
        api_key: "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"
    }
}))

router.post('/signup', (req, res) => {
    const { firstname, lastname, email, password, repassword } = req.body;

    if (!firstname || !lastname || !email || !password || !repassword) {
        return res.status(422).json({ error: "Please fill all the fields." })
    }
    if(!/^[a-zA-Z]{2,20}$/.test(firstname)){
        return res.status(422).json({ error: "First name must contain alphabets only." })
    }
    if (!/^[a-zA-Z]{2,30}$/.test(lastname)) {
        return res.status(422).json({ error: "Last name must contain alphabets only." })
    }
    if (!/\S+@\S+\.\S+/.test(email)) { //Very basic regex is used for email __@__.__
        return res.status(422).json({ error: "Invalid Email Address." })
    }
    if (!/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/.test(password)) {
        return res.status(422).json({ error: "Invalid Password: Must be atleast 8 characters long with 1 uppercase letter, 1 lowercase letter and 1 digit." })
    }
    if (password != repassword) {
        return res.status(422).json({ error: "Password does not match." })
    }
    User.findOne({ email: email })
        .then((savedUser) => {
            if (savedUser) {
                return res.status(422).json({ error: "A user is already registered with this Email Address." })
            }
            bcrypt.hash(password, 12)
                .then(password => {
                    const user = new User({
                        firstname,
                        lastname,
                        email,
                        password,
                        // repassword
                    })

                    user.save()
                        .then(user => {
                            transporter.sendMail({
                                to: user.email,
                                from: "allergyassistteam@gmail.com",
                                subject: "signup success",
                                html: "<h1>welcome to AllergyAssist</h1>"
                            })
                            res.json({ message: "Successfully Registered!" })
                        })
                        .catch(err => {
                            console.log(err)
                        })
                })

        })
        .catch(err => {
            console.log(err)
        })
})

router.post('/signin', (req, res) => {
    const { email, password } = req.body
    if (!email || !password) {
        return res.status(422).send({ error: "Please fill all the fields." })
    }
    // if (!/\S+@\S+\.\S+/.test(email)) { //Very basic regex is used for email __@__.__
    //     return res.status(422).json({ error: "Invalid Email Address format." })
    // }
    // if (!/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$/.test(password)) {
    //     return res.status(422).json({ error: "Invalid Password: Must be atleast 8 characters long with 1 uppercase letter, 1 lowercase letter and 1 digit." })
    // }
    User.findOne({ email: email })
        .then(savedUser => {
            if (!savedUser) {
                return res.status(422).json({ error: "Invalid Email Address." })
            }
            bcrypt.compare(password, savedUser.password)
                .then(doMatch => {
                    console.log(password)
                    console.log(savedUser.password)
                    if (doMatch) {
                        res.json({ message: "Login Successful!" })
                    }
                    else {
                        return res.status(422).json({ error: "Invalid Password." })
                    }
                })
                .catch(err => {
                    console.log(err)
                })
        })
})

router.post('/reset-password', (req, res) => {
    var otpCode = randomString({ length: 5 });
    crypto.randomBytes(32, (err, buffer) => {
        if (err) {
            console.log(err)
        }
        const { email } = req.body
        if (!email) {
            return res.status(422).send({ error: "Invalid Email Address." })
        }
        if (!/\S+@\S+\.\S+/.test(email)) { //Very basic regex is used for email __@__.__
            return res.status(422).json({ error: "Invalid Email Address Format." })
        }
        User.findOne({ email: email })
            .then(user => {
                if (!user) {
                    return res.status(422).json({ error: "Invalid Email Address." })
                }
                user.otpCode = otpCode
                user.save().then((result) => {
                    transporter.sendMail({
                        to: user.email,
                        from: "allergyassistteam@gmail.com",
                        subject: "password reset",
                        html: `<h2>Your OTP Code is : ${otpCode}</h2>`
                    })
                    res.json({ message: "OTP Code has been sent to your email address." })
                })

            })
    })
})

router.post('/otp', (req, res) => {
    const { email, otpCode } = req.body
    User.findOne({ email: email })
        .then(user => {
            if (user.otpCode != otpCode) {
                return res.status(422).json({ error: "Invalid OTP." })
            }
            else {
                res.json({ message: "OTP entered successfully." })
            }
        }).catch(err => {
            console.log(err)
        })
})

router.post('/new-password', (req, res) => {
    const newPassword = req.body.password
    const repassword = req.body.repassword
    const email = req.body.email
    if (newPassword != repassword) {
        return res.status(422).json({ error: "Password does not match." })
    }
    User.findOne({ email: email })
        .then(user => {
            bcrypt.hash(newPassword, 12).then(hashedpassword => {
                user.password = hashedpassword
                user.save().then((saveduser) => {
                    res.json("Password has been updated successfully!")
                })
            })
        }).catch(err => {
            console.log(err)
        })
})


module.exports = router
