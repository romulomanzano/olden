<template>
  <nav
    class="navbar navbar-vertical fixed-left navbar-expand-md navbar-light bg-white"
    id="sidenav-main"
  >
    <div class="container-fluid">
      <!--Toggler-->
      <navbar-toggle-button @click.native="showSidebar">
        <span class="navbar-toggler-icon"></span>
      </navbar-toggle-button>
      <router-link class="navbar-brand" to="/">
        <img :src="logo" class="navbar-brand-img" alt="..." />
      </router-link>

      <slot name="mobile-right">
        <ul class="nav align-items-center d-md-none">
          <base-dropdown class="nav-item" position="right">
            <div class="dropdown-header noti-title">
              <h6 class="text-overflow m-0">Account</h6>
            </div>
            <router-link to="/profile" class="dropdown-item">
              <i class="ni ni-single-02"></i>
              <span>My profile</span>
            </router-link>
            <div class="dropdown-divider"></div>
            <a href="#!" class="dropdown-item">
              <i class="ni ni-user-run"></i>
              <span>Logout</span>
            </a>
          </base-dropdown>
        </ul>
      </slot>
      <slot></slot>
      <div
        v-show="$sidebar.showSidebar"
        class="navbar-collapse collapse show"
        id="sidenav-collapse-main"
      >
        <div class="navbar-collapse-header d-md-none">
          <div class="row">
            <div class="col-6 collapse-brand">
              <router-link to="/">
                <img :src="logo" />
              </router-link>
            </div>
            <div class="col-6 collapse-close">
              <navbar-toggle-button
                @click.native="closeSidebar"
              ></navbar-toggle-button>
            </div>
          </div>
        </div>

        <ul class="navbar-nav">
          <slot name="links"> </slot>
        </ul>
        <!--coming soon-->
        <hr class="my-3" />
        <!--Heading-->
        <h6 class="navbar-heading text-muted">Comming Soon</h6>
        <!--Navigation-->
        <ul class="navbar-nav mb-md-3">
          <li>
            <div
              class="nav-link"
              @click="comingSoonMessage('This feature is not yet available.')"
            >
              <template class="nav-link">
                <i class="fa fa-inbox text-default"></i>
                <span class="nav-link-text">Members Messages</span>
              </template>
            </div>
          </li>
          <li class="nav-item">
            <div
              class="nav-link"
              @click="comingSoonMessage('This feature is not yet available.')"
            >
              <template>
                <i class="fa fa-envelope text-gray"></i>
                <span class="nav-link-text">Mail-in Orders</span>
              </template>
            </div>
          </li>
          <li class="nav-item">
            <div
              class="nav-link"
              @click="comingSoonMessage('This feature is not yet available.')"
            >
              <template>
                <i class="fa fa-users text-grey-dark"></i>
                <span class="nav-link-text">Team Management</span>
              </template>
            </div>
          </li>
        </ul>
        <!--Divider-->
        <hr class="my-3" />
        <!--Heading-->
        <h6 class="navbar-heading text-muted">Support</h6>
        <!--Navigation-->
        <ul class="navbar-nav mb-md-3">
          <li class="nav-item">
            <a class="nav-link" href="">
              <i class="fa fa-question-circle"></i> Contact Support
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
import NavbarToggleButton from "@/components/NavbarToggleButton";

export default {
  name: "sidebar",
  components: {
    NavbarToggleButton,
  },
  props: {
    logo: {
      type: String,
      default: "img/icons/large-192_x_192.png",
      description: "Olden logo",
    },
    autoClose: {
      type: Boolean,
      default: true,
      description:
        "Whether sidebar should autoclose on mobile when clicking an item",
    },
  },
  provide() {
    return {
      autoClose: this.autoClose,
    };
  },
  methods: {
    comingSoonMessage(featureName) {
      this.$message.info(featureName);
    },
    closeSidebar() {
      this.$sidebar.displaySidebar(false);
    },
    showSidebar() {
      this.$sidebar.displaySidebar(true);
    },
  },
  beforeDestroy() {
    if (this.$sidebar.showSidebar) {
      this.$sidebar.showSidebar = false;
    }
  },
};
</script>
