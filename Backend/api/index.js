const express = require('express')
const mysql = require('mysql2/promise')
const bcrypt = require('bcrypt')
const cors = require('cors')
const jwt = require('jsonwebtoken')

const app = express()
const port = 3000

app.use(cors());
app.use(express.json())

const secret = 'supersecret'

const initMySQL = async () => {
    conn = await mysql.createConnection({
        host: 'localhost',
        port: 3307,
        user: 'user1',
        password: 'mysql123456',
        database: 'my_db'
    })
}
app.listen(port, async (req, res) => {
    await initMySQL()
    console.log('server run at port ' + port)
})

app.get('/hello', (req, res) => {
    res.json({
        message: "hello!"
    })
})

app.post('/register', async (req, res) => {
    // "role" field in db default value = normal_user
    try {
        const {
            username,
            email,
            password
        } = req.body
        const passwordHash = await bcrypt.hash(password, 10)
        const role = "normal_user"
        const sql = "INSERT INTO web_users (username, email, password) VALUES (?, ?, ?)"
        const [CheckEmailDuplicate] = await conn.query('select email from web_users where email = ?', email)


        // หาก email ซ้ำให้ส่งไปเป็น 409 conflict ข้อมูลขัดแย้ง
        if (CheckEmailDuplicate.length > 0) {
            throw {
                statusCode: 409,
                message: 'email นี้ถูกใช้ไปแล้ว'
            }
        }

        await conn.query(sql, [username, email, passwordHash])
        res.json({
            message: 'Register success!'
        })
    } catch (error) {
        const status = error.statusCode || 500;
        res.status(status).json({
            message: "error, something wrong!",
            error: error.message
        })
    }
})

app.post('/login', async (req, res) => {
    try {
        const {
            email,
            password
        } = req.body
        const [results] = await conn.query('select * from web_users where email = ?', email)
        const userData = results[0]
        const match = await bcrypt.compare(password, userData.password)

        //หาก compare รหัสผ่านทั้งหน้าบ้านและหลังบ้านไม่ตรงให้ error login fail 
        if (!match) {
            res.status(400).json({
                message: 'login fail (wrong email or password)',
                states: false
            })
            return false
        }

        //หมดอายุใน 1 ชั่วโมง
        const token = jwt.sign({
            email
        }, secret, {
            expiresIn: '1h'
        })

        res.json({
            message: 'login success!',
            states: true,
            token
        })

    } catch (error) {
        res.status(401).json({
            message: 'login fail (wrong email or password)',
            states: false,
            error: error.message
        })
    }
})

app.get('/user', async (req, res) => {
    try {
        const {
            token
        } = req.body
        const email = jwt.verify(token, secret)

        res.json({
            message: 'login states ok',
            states: true
        })

    } catch (error) {
        const status = error.statusCode || 403;
        res.status(status).json({
            message: "error, Forbidded!",
            error: error.message,
            states: false
        })
    }
})

const verifyToken = (req, res, next) => {
    try {
        const authHeader = req.headers['authorization']
        const token = authHeader && authHeader.split(' ')[1]

        if (token == null) {
            throw {
                statusCode: 401,
            }
        }

        jwt.verify(token, secret, (err, user) => {
            if (err) {
                return res.sendStatus(403)
            }
            req.user = user
            next()
        })

    } catch (error) {
        const status = error.statusCode || 500;
        res.status(status).json({
            message: "error, something wrong!",
            error: error.message
        })
    }
}

app.get('/verify', verifyToken, (req, res) => {
    const email = req.user.email

    res.json({
        message: `verify success welcome, ${email}`
    })

    console.log(`verify success welcome, ${email}`)
})


app.post('/createsession', async (req, res) => {
    try {
        const {
            email,
            session,
            state
        } = req.body
        console.log(email)
        console.log(session)

        const sql = "INSERT INTO session_users (email, session_id, state) VALUES (?, ?, ?)"
        await conn.query(sql, [email, session, state])
        res.json({
            message: 'create session success!'
        })
    } catch (error) {
        res.status(500).json({
            message: "error, something wrong!",
            error: error.message
        })
    }
})

app.get('/getsession', async (req, res) => {
    try {
        const email = req.query.email
        const [results] = await conn.query('select session_id, state from session_users where email = ?', [email])
        res.json(results)
    } catch (error) {
        res.status(500).json({
            message: "error, something wrong!",
            error: error.message
        })
    }
})

app.delete('/deletesession', async (req, res) => {
    try {
        const session = req.query.session
        const sql = "DELETE FROM session_users WHERE session_id = ?"
        const [result] = await conn.query(sql, [session])
        console.log('delete session success!')
        res.json({
            message: "delete session success!"
        })
    } catch (error) {
        console.log(error)
        res.status(500).json({
            message: "error, something wrong!",
            error: error.message
        })
    }
})