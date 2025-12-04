const express = require('express')
const mysql = require('mysql2/promise')
const bcrypt = require('bcrypt')
const cors = require('cors')
const jwt = require('jsonwebtoken')

const app = express()
const port = 3000

app.use(cors());
app.use(express.json())

const secert = 'supersecret'

const initMySQL = async ()=>{
    conn = await mysql.createConnection({
        host: 'localhost',
        user: 'root',
        password: 'mysql123456',
        database: 'my_db'
    })
}
app.listen(port, async (req, res)=>{
    await initMySQL()
    console.log('server run at port '+ port)
})

app.get('/hello', (req, res)=>{
    res.json({
        message:"hello!"
    })
})

app.post('/register', async (req, res)=>{
    // "role" field in db default value = normal_user
    try{
        const {username, email, password} = req.body
        const passwordHash = await bcrypt.hash(password, 10)
        const role = "normal_user"
        const sql = "INSERT INTO web_users (username, email, password) VALUES (?, ?, ?)"
        const [CheckEmailDuplicate] = await conn.query('select email from web_users where email = ?', email)


        // หาก email ซ้ำให้ส่งไปเป็น 409 conflict ข้อมูลขัดแย้ง
        if(CheckEmailDuplicate.length>0){
            throw{
                statusCode: 409,
                message: 'email นี้ถูกใช้ไปแล้ว'
            }
        }

        await conn.query(sql, [username, email, passwordHash])
        res.json({
            message:'Register success!'
        })
    }catch(error){
        const status = error.statusCode || 500;
        res.status(status).json({
            message:"error, something wrong!",
            error: error.message
        })
    }
})

app.post('/login', async (req, res)=>{
    try{
        const {email, password} = req.body
        const [results] = await conn.query('select * from web_users where email = ?', email)
        const userData = results[0]
        const match = await bcrypt.compare(password, userData.password)

        //หาก compare รหัสผ่านทั้งหน้าบ้านและหลังบ้านไม่ตรงให้ error login fail 
        if(!match){
            res.status(400).json({
                message: 'login fail (wrong email or password)',
                states: false
            })
            return false
        }

        const token = jwt.sign({email}, secert, {expiresIn: '1h'})

        res.json({
           message:'login success!',
           states:true,
           token
        })
        
    }catch(error){
        res.status(401).json({
            message: 'login fail (wrong email or password)',
            states:false,
            error: error.message
        })
    }
})

app.get('/user', async (req, res)=>{
    try{
        const {token} = req.body
        const email = jwt.verify(token, secert)

        res.json({
            message:'login states ok',
            states:true
        })

    }catch(error){
        const status = error.statusCode || 403;
        res.status(status).json({
            message:"error, Forbidded!",
            error: error.message,
            states: false
        })
    }
})

