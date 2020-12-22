<template>
  <div>
    <base-header type="gradient-primary" class="pb-6 pb-8 pt-5 pt-md-8">
      <!-- Card stats -->
      <div class="row">
        <div class="col-xl-4 col-lg-6" @click="doCopy(instantMeetingLink)">
          <stats-card
            title="Instant Meeting Link"
            type="gradient-blue"
            :sub-title="instantMeetingLink"
            icon="fa fa-link"
            class="mb-4 mb-xl-0"
          >
          </stats-card>
        </div>
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
      </div>
    </base-header>

    <div>
      <modal
        :show="organizationNameMissing"
        body-classes="p-0"
        modal-classes="modal-dialog-centered modal-sm"
      >
        <card
          type="secondary"
          shadow
          header-classes="bg-white pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0"
        >
          <template>
            <div class="text-center text-muted mb-4">
              <h3>Enter Organization Name</h3>
            </div>
            <form role="form">
              <base-input
                alternative
                class="mb-3"
                v-model="editOrganizationName"
                @blur="$v.editOrganizationName.$touch()"
                :error="editOrganizationError"
              >
              </base-input>
              <div class="text-center">
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="!isFormValid"
                  @click="submitForm"
                  >Save</base-button
                >
              </div>
            </form>
          </template>
        </card>
      </modal>
    </div>
  </div>
</template>
<script>
import { required } from "vuelidate/lib/validators";
import axios from "../axios-auth";

const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);

export default {
  data() {
    return {
      upcomingEvents: 0,
      activeMembers: 0,
      pastEvents: 0,
      organizationNameMissing: null,
      editOrganizationName: null,
      instantMeetingLink: null,
    };
  },
  validations: {
    editOrganizationName: {
      required,
      isName: isValidStringWithSpaces,
    },
  },
  computed: {
    isFormValid() {
      return !this.$v.editOrganizationName.$invalid;
    },
    editOrganizationError() {
      if (this.editMode && this.$v.editOrganizationName.$error) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
  },
  methods: {
    doCopy(text) {
      this.$copyText(text);
      this.$message.success("Meeting URL Copied to Clipboard");
    },
    submitForm() {
      let data = {
        name: this.editOrganizationName,
      };
      axios
        .post(
          "organization/" + this.$store.state.organizationId + "/name/update",
          data
        )
        .then((res) => {
          this.$message.success(res.data.message);
          this.$store.dispatch(
            "updateOrganization",
            res.data.organization_details
          );
          this.organizationNameMissing =
            this.$store.state.organizationName === null;
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
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
      this.instantMeetingLink = data.instantMeetingLink;
    },
  },
  mounted() {
    this.getAccountSummary();
    this.organizationNameMissing =
      this.$store.state.organizationName === undefined;
  },
};
</script>
<style></style>
