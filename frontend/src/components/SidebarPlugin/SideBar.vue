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
        <img :src="logo" class="navbar-brand-img" alt="olden" />

        <h6 class="heading-small text-muted" v-if="orgName">
          {{ orgName }}
        </h6>
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
        <h6 class="navbar-heading text-muted">Coming Soon</h6>
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
            <a id="platform-tour" class="nav-link" @click="startTour()">
              <i class="fa fa-directions"></i> Menu Tour
            </a>
          </li>
          <li class="nav-item">
            <a
              class="nav-link"
              href="https://soundcare.typeform.com/to/hEebmPj3"
              target="_blank"
            >
              <i class="fa fa-question-circle"></i> Contact Us
            </a>
          </li>
        </ul>
      </div>
      <v-tour name="myTour" :steps="steps" class="tourbox"></v-tour>
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
  data() {
    return {
      steps: [
        {
          target: "#platform-tour", // We're using document.querySelector() under the hood
          header: {
            title: "Getting Started",
          },
          content: `Take the Tour`,
          params: {
            placement: "top", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: "#dashboard-element", // We're using document.querySelector() under the hood
          header: {
            title: "Dashboard",
          },
          content: `Account Summary`,
          params: {
            placement: "bottom", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: "#profile-element",
          content: "Update your profile",
          params: {
            placement: "top", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: "#virtual-events-element",
          content: "Create and manage events",
          params: {
            placement: "bottom", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
        {
          target: "#members-element",
          content: "Frequent event attendees",
          params: {
            placement: "bottom", // Any valid Popper.js placement. See https://popper.js.org/popper-documentation.html#Popper.placements
          },
        },
      ],
    };
  },
  props: {
    logo: {
      type: String,
      default: "img/icons/secondary-logo.png",
      description: "Olden logo",
    },
    autoClose: {
      type: Boolean,
      default: true,
      description:
        "Whether sidebar should autoclose on mobile when clicking an item",
    },
  },

  computed: {
    orgName() {
      return this.$store.state.organizationName;
    },
  },
  provide() {
    return {
      autoClose: this.autoClose,
    };
  },
  methods: {
    startTour() {
      this.$tours["myTour"].start();
    },
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
