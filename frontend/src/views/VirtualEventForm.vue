<template>
  <div>
    <base-header type="gradient-primary" class="pb-6 pb-8 pt-5 pt-md-8">
      <!-- Mask -->
    </base-header>

    <div class="container-fluid mt--8">
      <div class="row">
        <div class="col-xl-12 order-xl-1">
          <card shadow type="secondary">
            <div slot="header" class="bg-white border-0">
              <div class="row align-items-center">
                <div class="col-8">
                  <h3 class="mb-0">{{ eventName }}</h3>
                </div>
                <div class="col text-right">
                  <base-button
                    size="sm"
                    outline
                    icon="fa fa-edit"
                    slot="title"
                    type="secondary"
                    data-toggle="tooltip"
                    data-placement="left"
                    title="Edit Event Name"
                    @click="openForm"
                  >
                  </base-button>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col">
                <h6 class="heading-small text-muted mb-4">
                  When: {{ eventDate }}
                </h6>
              </div>

              <div class="col">
                <h6 class="heading-small text-muted mb-4">
                  Duration: {{ eventInfo.estimated_duration_minutes }} minutes
                </h6>
              </div>
            </div>
            <template>
              <form @submit.prevent>
                <tabs>
                  <tab-pane title="Attendees">
                    <div class="col">
                      <attendees-table
                        :eventId="eventId"
                        userType="attendee"
                        :phoneRequired="true"
                      ></attendees-table>
                    </div>
                  </tab-pane>
                  <tab-pane title="Alert Settings">
                    <div class="col">
                      <alert-settings-table
                        :eventId="eventId"
                      ></alert-settings-table>
                    </div>
                  </tab-pane>
                </tabs>
              </form>
            </template>
            <div>
              <modal
                :show.sync="editMode"
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
                      <h3>New Event Name</h3>
                    </div>
                    <form role="form">
                      <base-input
                        alternative
                        class="mb-3"
                        v-model="editEventName"
                        @blur="$v.editEventName.$touch()"
                        :error="eventNameError"
                      >
                      </base-input>
                      <div class="text-center">
                        <base-button
                          type="danger"
                          class="my-4"
                          @click="cancelEdit"
                          >Cancel</base-button
                        >
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
          </card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { required } from "vuelidate/lib/validators";
import axios from "../axios-auth";
import AttendeesTable from "./Tables/AttendeesTable";
import AlertSettingsTable from "./Tables/AlertSettingsTable";
import moment from "moment-timezone";

const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);

export default {
  name: "virtual-event-form",
  components: {
    AttendeesTable,
    AlertSettingsTable,
  },

  data() {
    return {
      eventName: "",
      eventId: null,
      editMode: false,
      editEventName: null,
      eventInfo: {},
    };
  },
  beforeMount() {
    if (this.$route.query.id) {
      this.eventId = this.$route.query.id;
      this.getVirtualEvent();
    } else {
      this.$router.push("virtual_events");
    }
  },
  computed: {
    eventDate() {
      return moment(this.eventInfo.date).format("LLL");
    },
    isFormValid() {
      return !this.$v.editEventName.$invalid;
    },
    eventNameError() {
      if (this.editMode && this.$v.editEventName.$error) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
  },
  validations: {
    editEventName: {
      required,
      isName: isValidStringWithSpaces,
    },
  },
  methods: {
    cancelEdit() {
      this.editMode = false;
      this.$v.$reset();
      this.editEventName = "";
    },
    openForm() {
      this.editEventName = "";
      this.$v.$reset();
      this.editMode = true;
    },
    submitForm() {
      this.editMode = false;
      let data = {
        eventInfo: {
          name: this.editEventName,
        },
      };
      axios
        .post(
          "organization/" +
            this.$store.state.organizationId +
            "/virtual_events/" +
            this.eventId +
            "/update",
          data
        )
        .then((res) => {
          this.$message.success(res.data.message);
          this.getVirtualEvent();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    getVirtualEvent() {
      axios
        .get(
          "organization/" +
            this.$store.state.organizationId +
            "/virtual_events/" +
            this.eventId,
          {}
        )
        .then((res) => {
          this.setEvent(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setEvent(data) {
      //personal info
      let eventInfo = data.event;
      this.eventName = eventInfo.name;
      this.eventId = eventInfo._id.$oid;
      this.eventInfo = data.event;
    },
  },
};
</script>
<style></style>
