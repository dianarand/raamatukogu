import axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000/';
axios.defaults.headers.common['Authorization'] = 'JWT ' + localStorage.getItem('token')