// src/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5005/',
  // Any other default properties
});

export default instance;
