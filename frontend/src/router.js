import Vue from "vue";
import Router from "vue-router";
import DashboardLayout from "@/layout/DashboardLayout";
import AuthLayout from "@/layout/AuthLayout";
import store from "./store";

Vue.use(Router);

export default new Router({
  linkExactActiveClass: "active",
  mode: "history",
  routes: [
    {
      path: "/",
      redirect: "dashboard",
      component: DashboardLayout,
      beforeEnter(to, from, next) {
        if (store.getters.isAuthenticated) {
          next({ path: next.path });
        } else {
          store.dispatch("tryAutoLogin");
          if (store.getters.isAuthenticated) {
            next({ path: to.path, query: to.query });
          } else {
            next({ path: "/login", query: to.query });
          }
        }
      },
      children: [
        {
          path: "/dashboard",
          name: "dashboard",
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () =>
            import(/* webpackChunkName: "demo" */ "./views/Dashboard.vue"),
        },
        {
          path: "/profile",
          name: "Profile",
          component: () =>
            import(/* webpackChunkName: "demo" */ "./views/UserProfile.vue"),
        },
        {
          path: "/virtual_events",
          name: "Virtual Events",
          component: () =>
            import(/* webpackChunkName: "demo" */ "./views/VirtualEvents.vue"),
        },
        {
          path: "/virtual_event",
          name: "virtual event",
          component: () =>
            import(
              /* webpackChunkName: "demo" */ "./views/VirtualEventForm.vue"
            ),
        },
      ],
    },
    {
      path: "/",
      redirect: "login",
      component: AuthLayout,
      beforeEnter(to, from, next) {
        if (store.getters.isAuthenticated) {
          next("/dashboard");
        } else {
          store.dispatch("tryAutoLogin");
          if (store.getters.isAuthenticated) {
            next("/dashboard");
          } else {
            next();
          }
        }
      },
      children: [
        {
          path: "/login",
          name: "login",
          component: () =>
            import(/* webpackChunkName: "demo" */ "./views/Login.vue"),
        },
      ],
    },
  ],
});
