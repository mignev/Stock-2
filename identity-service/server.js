const app = require('./app')

const dotenv = require('dotenv').config()

const PORT = process.env.PORT || 3000

app.listen(PORT, () => console.log('Identity service listening in port', PORT))