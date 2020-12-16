<template>
  <div>
    <div class="row align-items-center">
      <div class="col">
        <h6 class="heading-small text-muted mb-4">
          {{ title }}
        </h6>
      </div>
      <div class="col text-right">
        <base-button
          type="primary"
          size="sm"
          v-if="!modalVirtualEventMode"
          @click="openModal"
          >Schedule New Event</base-button
        >
      </div>
    </div>
    <div>
      <modal
        :show.sync="modalVirtualEventMode"
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
              <h3>Enter Event Details</h3>
            </div>
            <form role="form">
              <base-input
                alternative
                class="mb-3"
                v-model="modalVirtualEventName"
                placeholder="Event Name"
                @blur="$v.modalVirtualEventName.$touch()"
                :error="isValidPlanNameError"
              >
              </base-input>
              <base-input addon-left-icon="ni ni-calendar-grid-58">
                <flat-picker
                  slot-scope="{ focus, blur }"
                  @on-open="focus"
                  @on-close="blur"
                  :config="{ allowInput: true, enableTime: true }"
                  class="form-control datepicker"
                  v-model="modalVirtualDate"
                >
                </flat-picker>
              </base-input>
              <base-input>
                <v-select
                  v-model="modalVirtualDateTimezone"
                  label="countryName"
                  :options="timezones"
                ></v-select>
              </base-input>
              <div class="text-center">
                <base-button type="danger" class="my-4" @click="closeModal"
                  >Cancel</base-button
                >
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="!isModalFormValid"
                  @click="submitVirtualEvent"
                  >Submit</base-button
                >
              </div>
            </form>
          </template>
        </card>
      </modal>
    </div>
    <div class="table-responsive">
      <base-table
        class="table align-items-center table-flush"
        :class="type === 'dark' ? 'table-dark' : ''"
        :thead-classes="type === 'dark' ? 'thead-dark' : 'thead-light'"
        tbody-classes="list"
        :data="VirtualEventList"
      >
        <template slot="columns">
          <th>Event Name</th>
          <th>Date</th>
          <th>Registered</th>
          <th>Duration (Minutes)</th>
          <th></th>
        </template>

        <template slot-scope="{ row }">
          <th scope="row">
            {{ row.name | capitalize }}
          </th>
          <td class="budget">
            {{ new Date(row.date.$date) | moment("dddd, MMMM Do YYYY") }}
          </td>
          <td class="budget">
            {{
              new Date(row.registered_date.$date) | moment("dddd, MMMM Do YYYY")
            }}
          </td>
          <th scope="row">
            {{ row.estimated_duration_minutes }}
          </th>
          <td class="text-right">
            <base-button
              type="primary"
              outline
              size="sm"
              icon="fa fa-pen"
              @click="editMode(row)"
              >Edit</base-button
            >
            <base-button
              type="danger"
              outline
              size="sm"
              icon="fa fa-trash"
              @click="archiveMode(row._id.$oid)"
              >Archive</base-button
            >
          </td>
        </template>
      </base-table>
      <modal
        :show.sync="archiveVirtualEventMode"
        gradient="primary"
        modal-classes="modal-primary modal-dialog-centered"
      >
        <div class="py-3 text-center">
          <i class="ni ni-bell-55 ni-3x"></i>
          <h4 class="heading mt-4">Cancel Virtual Event</h4>
          <p>
            This will cancel this event, users will be notified this event will
            no longer take place.
          </p>
        </div>

        <template slot="footer">
          <base-button
            type="link"
            text-color="white"
            class="mr-auto"
            @click="closeDeregisterModal"
          >
            Go Back
          </base-button>
          <base-button class="ml-auto" type="white" @click="archiveVirtualEvent"
            >Cancel anyways</base-button
          >
        </template>
      </modal>
    </div>
  </div>
</template>
<script>
import axios from "../../axios-auth";
import { required } from "vuelidate/lib/validators";
import flatPicker from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
import moment_timezone from "moment-timezone";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);

export default {
  name: "virtual-events-table",
  components: {
    flatPicker,
    vSelect,
  },
  props: {
    type: {
      type: String,
    },
    title: String,
  },
  mounted() {
    this.timezones = moment_timezone.tz.names();
    this.getUserVirtualEvents();
  },
  data() {
    return {
      VirtualEventList: [],
      modalVirtualEventName: null,
      modalVirtualDate: null,
      modalVirtualEventMode: null,
      modalVirtualDateTimezone: null,
      archiveVirtualEventMode: false,
      archiveVirtualEventId: null,
      recipientList: null,
      timezones: [],
    };
  },
  validations: {
    modalVirtualEventName: {
      required,
      isName: isValidStringWithSpaces,
    },
  },
  computed: {
    isModalFormValid() {
      return !this.$v.modalVirtualEventName.$invalid;
    },
    isValidPlanNameError() {
      if (this.modalVirtualEventMode && this.$v.modalVirtualEventName.$error) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
  },
  methods: {
    getUserVirtualEvents() {
      axios
        .get("virtual_events/user/virtual_events", {})
        .then((res) => {
          this.setVirtualEvents(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setVirtualEvents(data) {
      this.VirtualEventList = data;
    },
    closeModal() {
      this.modalVirtualEventMode = false;
      this.modalVirtualEventName = null;
    },
    openModal() {
      this.modalVirtualEventMode = true;
      this.$v.$reset();
    },
    submitVirtualEvent() {
      //post to backend
      let data = {
        modalVirtualEventName: this.modalVirtualEventName,
      };
      this.closeModal();
      //depending of the value either post new or update virtual event
      axios
        .post("virtual_events/user/virtual_events/add", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.$router.push(
            "virtual_event?id=" + res.data.virtual_event._id.$oid
          );
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    archiveMode(eventId) {
      this.archiveVirtualEventId = eventId;
      this.archiveVirtualEventMode = true;
    },
    editMode(row) {
      this.$v.$reset();
      //set to pre-existing values
      this.$router.push("virtual_event?id=" + row._id.$oid);
    },
    closeDeregisterModal() {
      this.archiveVirtualEventMode = false;
    },
    archiveVirtualEvent() {
      //post to backend
      let planId = this.archiveVirtualEventId;
      this.closeDeregisterModal();
      axios
        .post("virtual_events/user/virtual_event/" + planId + "/cancel", {})
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUserVirtualEvents();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
  },
};
</script>
<style>
.vs__search,
.vs__search:focus {
  margin: 0px 0 0;
  padding: 0 0px;
  background: white;
}

.vs--single .vs__selected {
  /* background-color: transparent; */
  /* border-color: transparent; */
  background-color: white;
  border-color: white;
}

.vs__selected {
  /* margin: 4px 2px 0; */
  /* padding: 0 .25em; */
  margin: 0;
  padding: 0;
}
</style>
