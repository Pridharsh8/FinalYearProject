const route=require('express')
const router=route()

const authcontroller= require('../controller/authcontroller')
router.post('/signup',authcontroller.signup_post)
router.post('/login',authcontroller.login_post)


module.exports=router