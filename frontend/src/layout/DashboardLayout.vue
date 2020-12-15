<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
    <side-bar
      :background-color="sidebarBackground"
      short-title="Argon"
      title="Argon"
    >
      <template slot="links">
        <sidebar-item
          :link="{
            name: 'Dashboard',
            icon: 'ni ni-tv-2 text-primary',
            path: '/dashboard',
          }"
        />

        <sidebar-item
          :link="{
            name: 'User Profile',
            icon: 'ni ni-single-02 text-yellow',
            path: '/profile',
          }"
        />
        <sidebar-item
          :link="{
            name: 'Safety Plans',
            icon: 'fa fa-life-ring text-red',
            path: '/safety_plans',
          }"
        />

        <template>
          <li class="nav-item">
            <router-link
              to=""
              class="nav-link"
              target=""
              href=""
              @click.native="
                comingSoonMessage('Virtual Care is not yet available.')
              "
            >
              <template>
                <i class="fa fa-laptop-medical text-purple"></i>
                <span class="nav-link-text">Virtual Care</span>
              </template>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              to=""
              class="nav-link"
              target=""
              href=""
              @click.native="
                comingSoonMessage(
                  'Companionship Programs are not yet available.'
                )
              "
            >
              <template>
                <i class="fa fa-user-friends text-gray"></i>
                <span class="nav-link-text">Recreational Plans</span>
              </template>
            </router-link>
          </li>
        </template>
      </template>
    </side-bar>
    <div class="main-content" :data="sidebarBackground">
      <dashboard-navbar></dashboard-navbar>

      <div @click="toggleSidebar">
        <fade-transition :duration="200" origin="center top" mode="out-in">
          <!-- your content here -->
          <router-view></router-view>
        </fade-transition>
        <div class="container sticky-bottom mb-2">
          <content-footer v-if="!$route.meta.hideFooter"></content-footer>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import DashboardNavbar from "./DashboardNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import { FadeTransition } from "vue2-transitions";

export default {
  components: {
    DashboardNavbar,
    ContentFooter,
    FadeTransition,
  },
  data() {
    return {
      sidebarBackground: "vue", //vue|blue|orange|green|red|primary
    };
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    },
    comingSoonMessage(featureName) {
      this.$message.info(featureName);
    },
  },
};
</script>
<style lang="scss"></style>
