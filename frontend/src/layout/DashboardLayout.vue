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
            icon: 'fa fa-user-cog text-blue',
            path: '/profile',
          }"
        />
        <sidebar-item
          :link="{
            name: 'Virtual Events',
            icon: 'fa fa-life-ring text-primary',
            path: '/virtual_events',
          }"
        />
        <sidebar-item
          :link="{
            name: 'Members',
            icon: 'fa fa-user-plus text-purple',
            path: '/members',
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
                comingSoonMessage('This feature is not yet available.')
              "
            >
              <template>
                <i class="fa fa-inbox text-default"></i>
                <span class="nav-link-text">Members Messages</span>
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
                comingSoonMessage('This feature is not yet available.')
              "
            >
              <template>
                <i class="fa fa-envelope text-gray"></i>
                <span class="nav-link-text">Mail-in Orders</span>
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
                comingSoonMessage('This feature is not yet available.')
              "
            >
              <template>
                <i class="fa fa-users text-grey-dark"></i>
                <span class="nav-link-text">Team Management</span>
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
