<template>
  <div>
    <base-header type="gradient-primary" class="pb-6 pb-8 pt-5 pt-md-8">
      <!-- Card stats -->
      <div class="row">
        <div class="col-xl-4 col-lg-6">
          <stats-card
            title="Upcoming Events"
            type="gradient-primary"
            v-bind:sub-title="upcomingEvents | formatNumber"
            icon="fa fa-calendar"
            class="mb-4 mb-xl-0"
          >
          </stats-card>
        </div>
        <div class="col-xl-4 col-lg-6">
          <stats-card
            title="Active Members"
            type="gradient-purple"
            :sub-title="activeMembers | formatNumber"
            icon="fa fa-address-card"
            class="mb-4 mb-xl-0"
          >
          </stats-card>
        </div>
        <div class="col-xl-4 col-lg-6">
          <stats-card
            title="Past Events"
            type="gradient-danger"
            :sub-title="pastEvents | formatNumber"
            icon="fa fa-calendar-check"
            class="mb-4 mb-xl-0"
          >
          </stats-card>
        </div>
      </div>
    </base-header>
  </div>
</template>
<script>
import axios from "../axios-auth";

export default {
  data() {
    return {
      upcomingEvents: 0,
      activeMembers: 0,
      pastEvents: 0,
    };
  },
  methods: {
    getAccountSummary() {
      axios
        .get(
          "organization/" +
            this.$store.state.organizationId +
            "/account_summary",
          {}
        )
        .then((res) => {
          this.setSummary(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setSummary(data) {
      this.upcomingEvents = data.upcoming_events;
      this.activeMembers = data.active_members;
      this.pastEvents = data.past_events;
    },
  },
  mounted() {
    this.getAccountSummary();
  },
};
</script>
<style></style>
