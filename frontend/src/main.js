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
import VueClipboard from "vue-clipboard2";
import * as Sentry from "@sentry/browser";
import { Integrations } from "@sentry/tracing";
import { Vue as VueIntegration } from "@sentry/integrations";
import { Integrations as ApmIntegrations } from "@sentry/apm";
import VueTour from "vue-tour";

require("vue-tour/dist/vue-tour.css");

Sentry.init({
  Vue,
  dsn:
    "https://07c798e2e1de4ab2bb95dd505836d4a6@o495064.ingest.sentry.io/5567215",
  environment: process.env.NODE_ENV,
  autoSessionTracking: true,
  integrations(integrations) {
    integrations.push(
      new VueIntegration({
        attachProps: true,
        logErrors: true,
      })
    );
    integrations.push(new ApmIntegrations.Tracing());
    integrations.push(new Integrations.BrowserTracing());
    return integrations;
  },
  // We recommend adjusting this value in production, or using tracesSampler
  // for finer control
  tracesSampleRate: 1.0,
});

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
Vue.use(VueClipboard);
Vue.use(VueTour);

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
