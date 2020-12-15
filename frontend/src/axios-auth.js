import axios from "axios";
let isProd = process.env.NODE_ENV === "production";

const instance = axios.create({
  baseURL: isProd ? "https://api.olden.ai" : "http://localhost:3000/",
});

export default instance;
