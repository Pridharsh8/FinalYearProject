const mongoose= require('mongoose')
const Schema=mongoose.Schema
const userSchema= new Schema(
    {
       
        mail:{
            type:String,
            required:[true, 'Please enter an email'],
            unique:true
        },
        password:{
            type:String,
            required:[true, 'Please enter an password'],
            minLength:[6,'Minimum password length is 6']
        }
    }
)

// userSchema.post('save',function(doc,next){
//     console.log("New user was created")
// })

module.exports= mongoose.model("user",userSchema)