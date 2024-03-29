import Vue from "vue";
import Vuex from "vuex";
import axios from "./axios-auth";
import router from "./router";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    userToken: null,
    userId: null,
    userEmail: null,
    organizationId: null,
    organizationName: null,
  },
  mutations: {
    authUser(state, userData) {
      state.userToken = userData.userToken;
      state.userId = userData.userId;
      state.userEmail = userData.userEmail;
      state.organizationId = userData.organizationId;
      state.organizationName = userData.organizationName;
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${userData.userToken}`;
    },
    clearAuthData(state) {
      state.userToken = null;
      state.userId = null;
      state.userEmail = null;
      state.organizationId = null;
      state.organizationName = null;
      axios.defaults.headers.common["Authorization"] = null;
    },
    updateOrganizationData(state, data) {
      state.organizationId = data.organizationId;
      state.organizationName = data.organizationName;
    },
  },
  actions: {
    setOrganization({ commit }, organizationDetails) {
      try {
        commit("updateOrganizationData", organizationDetails);
        localStorage.setItem(
          "organizationId",
          organizationDetails.organizationId
        );
        localStorage.setItem(
          "organizationName",
          organizationDetails.organizationName
        );
      } catch (error) {
        Vue.$log.debug(error);
      }
    },
    authenticateUser({ commit, dispatch }, authData) {
      commit("authUser", {
        userToken: authData.userToken,
        userId: authData.userId,
        userEmail: authData.userEmail,
        organizationId: authData.organizationId,
        organizationName: authData.organizationName,
      });
      dispatch("setLogoutTimer", authData.expiresIn);
      const now = new Date();
      const expirationDate = new Date(
        now.getTime() + authData.expiresIn * 1000
      );
      localStorage.setItem("userToken", authData.userToken);
      localStorage.setItem("userId", authData.userId);
      localStorage.setItem("expirationDate", expirationDate);
      localStorage.setItem("userEmail", authData.userEmail);
      localStorage.setItem("organizationId", authData.organizationId);
      localStorage.setItem("organizationName", authData.organizationName);
      router.replace("/dashboard");
    },
    setLogoutTimer({ commit }, expirationTime) {
      setTimeout(() => {
        commit("clearAuthData");
      }, expirationTime * 1000);
    },
    async login({ dispatch }, data) {
      try {
        await dispatch("authenticateUser", {
          userToken: data.userToken,
          userId: data.userId,
          expiresIn: data.expiresIn,
          userEmail: data.userEmail,
          organizationId: data.organizationId,
          organizationName: data.organizationName,
        });
      } catch (error) {
        Vue.$log.debug(error);
      }
    },
    async updateOrganization({ dispatch }, data) {
      try {
        await dispatch("setOrganization", {
          organizationId: data.organizationId,
          organizationName: data.organizationName,
        });
      } catch (error) {
        Vue.$log.debug(error);
      }
    },
    tryAutoLogin({ commit, dispatch }) {
      const userToken = localStorage.getItem("userToken");
      if (!userToken) {
        return;
      }
      const expirationDate = new Date(localStorage.getItem("expirationDate"));
      const now = new Date();
      if (now >= expirationDate) {
        dispatch("logout");
        return;
      }
      const userId = localStorage.getItem("userId");
      const userEmail = localStorage.getItem("userEmail");
      const organizationId = localStorage.getItem("organizationId");
      const organizationName = localStorage.getItem("organizationName");
      commit("authUser", {
        userToken: userToken,
        userId: userId,
        userEmail: userEmail,
        organizationId: organizationId,
        organizationName: organizationName,
      });
      router.replace("/dashboard");
    },
    logout({ commit }) {
      commit("clearAuthData");
      localStorage.removeItem("expirationDate");
      localStorage.removeItem("userId");
      localStorage.removeItem("userToken");
      localStorage.removeItem("userEmail");
      localStorage.removeItem("organizationId");
      localStorage.removeItem("organizationName");
      router.replace("/login");
    },
  },
  getters: {
    isAuthenticated(state) {
      return state.userToken !== null;
    },
  },
});
