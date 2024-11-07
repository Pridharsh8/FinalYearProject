const express=require('express')
require("dotenv").config()
const cors=require('cors')
const bodyParser = require('body-parser');
const mongoose=require('mongoose')
const lodash=require('lodash')

const userRoute=require('./route/userroute')


const app=express()
app.use(express.json());
const session = require('express-session');
app.set('view engine', 'ejs');



mongoose.connect(process.env.MONGODB_URI).then(()=>{
    console.log("Success")
    app.listen(process.env.PORT_NO,()=>{
        console.log("Server is listening");
    });
})
.catch((e)=> console.log(e));

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));


app.use(cors());

app.use('/',userRoute)
