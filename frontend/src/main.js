import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import "./registerServiceWorker";
import ArgonDashboard from "./plugins/argon-dashboard";
import store from "./store";
import Message from "vue-m-message";
import Vuelidate from "vuelidate";
import VueLogger from "vuejs-logger";
import VueMoment from "vue-moment";
import numeral from "numeral";
import VueConstants from "vue-constants";

Vue.config.productionTip = false;
const isProduction = process.env.NODE_ENV === "production";

const options = {
  isEnabled: true,
  logLevel: isProduction ? "error" : "debug",
  stringifyArguments: false,
  showLogLevel: true,
  showMethodName: true,
  separator: "|",
  showConsoleColors: true,
};

Vue.use(ArgonDashboard);
Vue.use(Message);
Vue.use(Vuelidate);
Vue.use(VueLogger, options);
Vue.use(VueMoment);
Vue.use(VueConstants);

//Add some filters
Vue.filter("capitalize", function (value) {
  if (!value) return "";
  value = value.toString();
  return value.charAt(0).toUpperCase() + value.slice(1);
});

Vue.filter("formatNumber", function (value) {
  return numeral(value).format("0,0"); // displaying other groupings/separators is possible, look at the docs
});

Vue.filter("formatPercentage", function (value) {
  return numeral(value).format("0.0%");
});

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
