const express = require("express");
const path = require('path');
const bodyParser = require("body-parser");

const app = express();

const ViewsDir = path.join((__dirname, ''));
app.set('views', ViewsDir);
app.set('view engine', 'pug');
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

app.get("/", (req, res) => {
	console.log("hello");
	return res.render('index', {
		quantity_t: '',
		quantity_e: '',
		reenter_t: '',
		reenter_e: '',
		queue_t: '',
		queue_e: '',
	});
})

app.post("/calculate", (req, res) => {
	const {a, b, lambda, request_quantity, reentry_probability, delta_t} = req.body;
	let m_quantity_t = 'test';
	let m_quantity_e = 'test';
	let m_reenter_t = 'test';
	let m_reenter_e = 'test';
	let m_queue_t = 'test';
	let m_queue_e = 'test';

	return res.render('index', {
		quantity_t: m_quantity_t,
		quantity_e: m_quantity_e,
		reenter_t: m_reenter_t,
		reenter_e: m_reenter_e,
		queue_t: m_queue_t,
		queue_e: m_queue_e,
	});
})

app.listen(8000);
