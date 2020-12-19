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
        v-model="alertSettings.sms"
        :disabled="updatesDisabled"
      >
        SMS Alerts
      </base-checkbox>
      <base-checkbox
        class="mb-3"
        v-model="alertSettings.email"
        :disabled="updatesDisabled"
      >
        Email
      </base-checkbox>
      <base-checkbox
        class="mb-3"
        v-model="alertSettings.prerecorded_voice"
        :disabled="true"
      >
        Pre-recorded Voice Alerts
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
  name: "alert-settings-table",
  props: {
    eventId: {
      type: String,
      description: "Event id.",
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
        (this.originalSettings.sms !== this.alertSettings.sms) |
        (this.originalSettings.email !== this.alertSettings.email) |
        (this.originalSettings.prerecorded_voice !==
          this.alertSettings.prerecorded_voice)
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
          sms: this.alertSettings.sms,
          email: this.alertSettings.email,
          prerecorded_voice: this.alertSettings.prerecorded_voice,
        },
      };
      axios
        .post(
          "organization/" +
            this.$store.state.organizationId +
            "/virtual_events/" +
            this.eventId +
            "/alert_settings/update",
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
          "organization/" +
            this.$store.state.organizationId +
            "/virtual_events/" +
            this.eventId +
            "/alert_settings",
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
