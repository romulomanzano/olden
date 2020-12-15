<template>
  <div>
    <div class="row align-items-center">
      <div class="col">
        <h6 class="heading-small text-muted mb-4">
          Alert Settings
        </h6>
      </div>
    </div>
    <div>
      <base-checkbox
        class="mb-3"
        v-model="alertSettings.inactivity"
        :disabled="updatesDisabled"
      >
        Inactivity Alerts
      </base-checkbox>
      <base-checkbox
        class="mb-3"
        v-model="alertSettings.fall_detection"
        :disabled="updatesDisabled"
      >
        Fall Detection Alerts
      </base-checkbox>
      <base-checkbox
        class="mb-3"
        v-model="alertSettings.daily_report"
        :disabled="updatesDisabled"
      >
        Daily Summary Report
      </base-checkbox>
      <template v-if="changesMade">
        <base-button
          type="danger"
          size="sm"
          icon="fa fa-save"
          :disabled="!changesMade"
          @click="updateSettings"
          >Save Changes</base-button
        >
      </template>
    </div>
  </div>
</template>
<script>
import axios from "../../axios-auth";

export default {
  name: "safety-plan-user-table",
  props: {
    planId: {
      type: String,
      description: "Plan id.",
    },
  },
  data() {
    return {
      alertSettings: {},
      originalSettings: {},
      updatesDisabled: false,
    };
  },
  mounted() {
    this.getAlertSettings();
  },
  computed: {
    changesMade() {
      return (
        (this.originalSettings.fall_detection !==
          this.alertSettings.fall_detection) |
        (this.originalSettings.daily_report !==
          this.alertSettings.daily_report) |
        (this.originalSettings.inactivity !== this.alertSettings.inactivity)
      );
    },
  },
  methods: {
    disableUpdates() {
      this.updatesDisabled = true;
    },
    enableUpdates() {
      this.updatesDisabled = false;
    },
    updateSettings() {
      this.disableUpdates();
      let data = {
        alertSettings: {
          inactivity: this.alertSettings.inactivity,
          fall_detection: this.alertSettings.fall_detection,
          daily_report: this.alertSettings.daily_report,
        },
      };
      axios
        .post(
          "safety/user/safety_plan/" + this.planId + "/alert_settings/update",
          data
        )
        .then((res) => {
          this.$message.success(res.data.message);
          this.getAlertSettings();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    getAlertSettings() {
      axios
        .get(
          "safety/user/safety_plan/" + this.planId + "/alert_settings/get",
          {}
        )
        .then((res) => {
          this.setSettings(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setSettings(data) {
      this.alertSettings = Object.assign({}, data);
      this.originalSettings = Object.assign({}, data);
      this.enableUpdates();
    },
  },
};
</script>
