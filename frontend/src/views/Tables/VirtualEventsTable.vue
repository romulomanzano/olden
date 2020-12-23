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
            <form role="form" @submit.prevent="">
              <base-input
                alternative
                class="mb-3"
                v-model="modalVirtualEventName"
                placeholder="Event Name"
                @blur="$v.modalVirtualEventName.$touch()"
                :error="isValidEventNameError"
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
                  @blur="$v.modalVirtualDate.$touch()"
                  :error="isValidEventDateError"
                >
                </flat-picker>
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
          <th>Created</th>
          <th>Meeting Link</th>
          <th></th>
        </template>

        <template slot-scope="{ row }">
          <td scope="row">
            {{ row.name | capitalize }}
          </td>
          <td class="budget" v-if="row.date">
            {{ toMomentLocale(row.date) }}
          </td>
          <td v-else>
            N/A
          </td>

          <td class="budget" v-if="row.created_date">
            {{ toMomentLocale(row.created_date) }}
          </td>
          <td v-else>
            N/A
          </td>
          <td scope="row" v-if="row.meeting_details">
            <base-button
              size="sm"
              type="default"
              outline
              icon="fa fa-copy"
              @click="doCopy(row.meeting_details.url)"
            ></base-button>
            {{ (row.meeting_details || {}).url }}
          </td>
          <td v-else>
            -
          </td>
          <td class="text-right">
            <base-button
              type="primary"
              outline
              size="sm"
              icon="fa fa-pen"
              @click="editMode(row)"
              >Manage</base-button
            >
            <base-button
              type="danger"
              outline
              size="sm"
              icon="fa fa-trash"
              @click="archiveMode(row._id.$oid)"
              >Cancel</base-button
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
import moment from "moment-timezone";

const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);

export default {
  name: "virtual-events-table",
  components: {
    flatPicker,
  },
  props: {
    type: {
      type: String,
    },
    title: String,
  },
  mounted() {
    this.getUserVirtualEvents();
    this.localTimezone = moment.tz.guess();
  },
  data() {
    return {
      VirtualEventList: [],
      modalVirtualEventName: null,
      modalVirtualDate: null,
      modalVirtualEventMode: null,
      localTimezone: null,
      archiveVirtualEventMode: false,
      archiveVirtualEventId: null,
      recipientList: null,
    };
  },
  validations: {
    modalVirtualEventName: {
      required,
      isName: isValidStringWithSpaces,
    },
    modalVirtualDate: {
      required,
    },
  },
  computed: {
    isModalFormValid() {
      return (
        !this.$v.modalVirtualEventName.$invalid &&
        !this.$v.modalVirtualDate.$invalid
      );
    },
    isValidEventNameError() {
      if (this.modalVirtualEventMode && this.$v.modalVirtualEventName.$error) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    isValidEventDateError() {
      if (this.modalVirtualDate && this.$v.modalVirtualDate.$error) {
        return "You must set a date and a time.";
      }
      return "";
    },
    modalVirtualDateUtc: function () {
      // `this` points to the vm instance
      return moment(this.modalVirtualDate).utc().format("YYYY-MM-DDTHH:mm[Z]");
    },
  },
  methods: {
    toMomentLocale(input) {
      return moment(input).format("LLL");
    },
    getUserVirtualEvents() {
      axios
        .get(
          "organization/" +
            this.$store.state.organizationId +
            "/virtual_events",
          { params: { type: this.type } }
        )
        .then((res) => {
          this.setVirtualEvents(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setVirtualEvents(data) {
      this.VirtualEventList = data.events;
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
        eventName: this.modalVirtualEventName,
        eventDatetime: this.modalVirtualDateUtc,
        createdUnderTimezone: this.localTimezone,
      };
      this.closeModal();
      //depending of the value either post new or update virtual event
      axios
        .post(
          "organization/" +
            this.$store.state.organizationId +
            "/virtual_events/add",
          data
        )
        .then((res) => {
          this.$message.success(res.data.message);
          this.$router.push(
            "virtual_event?id=" + res.data.virtual_event._id.$oid
          );
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    doCopy(text) {
      this.$copyText(text);
      this.$message.success("Meeting URL Copied to Clipboard");
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
        .post(
          "organization/" +
            this.$store.state.organizationId +
            "/virtual_events/" +
            planId +
            "/cancel",
          {}
        )
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
