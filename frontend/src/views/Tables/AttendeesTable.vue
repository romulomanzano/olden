<template>
  <div>
    <div class="row align-items-center">
      <div class="col">
        <h6 class="heading-small text-muted mb-4">
          {{ userType | capitalize }}S
        </h6>
      </div>
      <div class="col text-right">
        <base-button
          type="primary"
          size="sm"
          v-if="!addUserMode"
          @click="openUserModal"
          >Add {{ userType | capitalize }}</base-button
        >
      </div>
    </div>
    <div class="table-responsive">
      <base-table
        class="table align-items-center table-flush"
        tbody-classes="list"
        :data="userList"
      >
        <template slot="columns">
          <th>First Name</th>
          <th>Last Name</th>
          <th>Email</th>
          <th v-if="phoneRequired">Phone Number</th>
          <th></th>
        </template>

        <template slot-scope="{ row }">
          <th scope="row">
            {{ row.first_name | capitalize }}
          </th>
          <th scope="row">
            {{ row.last_name | capitalize }}
          </th>
          <th scope="row">
            {{ row.email }}
          </th>

          <th v-if="phoneRequired" scope="row">
            {{ row.phone_number }}
          </th>
          <td class="text-right">
            <base-button
              type="danger"
              data-toggle="tooltip"
              data-placement="top"
              title="Remove from event"
              outline
              size="sm"
              icon="fa fa-trash"
              @click="openRemoveUserModal(row._id.$oid)"
              >Remove</base-button
            >
          </td>
        </template>
      </base-table>
      <div>
        <modal
          :show.sync="addUserMode"
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
                <h3>Enter User Details</h3>
              </div>
              <form role="form">
                <base-input
                  alternative
                  class="mb-3"
                  v-model="addUserFirstName"
                  placeholder="First Name"
                  @blur="$v.addUserFirstName.$touch()"
                  :error="isValidUserFirstNameError"
                >
                </base-input>
                <base-input
                  alternative
                  class="mb-3"
                  v-model="addUserLastName"
                  placeholder="Last Name"
                  @blur="$v.addUserLastName.$touch()"
                  :error="isValidUserLastNameError"
                >
                </base-input>
                <base-input
                  v-model="addUserEmail"
                  @blur="$v.addUserEmail.$touch()"
                  alternative
                  class="mb-3"
                  placeholder="Email"
                  addon-left-icon="ni ni-email-83"
                  name="email"
                  :error="isValidUserEmailError"
                >
                </base-input>
                <base-input
                  v-if="phoneRequired"
                  v-model="addUserPhoneNumber"
                  @blur="$v.addUserPhoneNumber.$touch()"
                  alternative
                  class="mb-3"
                  placeholder="Phone"
                  addon-left-icon="fa fa-phone"
                  name="phone"
                  :error="isValidUserPhoneNumberError"
                >
                </base-input>

                <div class="text-center">
                  <base-button
                    type="danger"
                    class="my-4"
                    @click="closeAddUserModal"
                    >Cancel</base-button
                  >
                  <base-button
                    type="primary"
                    class="my-4"
                    :disabled="!isAddUserModalValid"
                    @click="addUserSubmit"
                    >Submit</base-button
                  >
                </div>
              </form>
            </template>
          </card>
        </modal>
      </div>

      <modal
        :show.sync="removeUserMode"
        gradient="primary"
        modal-classes="modal-primary modal-dialog-centered"
      >
        <div class="py-3 text-center">
          <i class="ni ni-bell-55 ni-3x"></i>
          <h4 class="heading mt-4">
            Remove {{ userType | capitalize }} from Event
          </h4>
          <p>
            This will remove this {{ userType }} from the event, we will send
            them a notification letting them know the event has been canceled.
          </p>
        </div>

        <template slot="footer">
          <base-button
            type="link"
            text-color="white"
            class="mr-auto"
            @click="closeRemoveUserModal"
          >
            Cancel
          </base-button>
          <base-button class="ml-auto" type="white" @click="removeUser"
            >Remove anyways</base-button
          >
        </template>
      </modal>
    </div>
  </div>
</template>
<script>
import { email, required } from "vuelidate/lib/validators";
import axios from "../../axios-auth";

const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);
const isPhone = (value) => /^[0-9]{10}$/.test(value);

export default {
  name: "attendees-table",
  props: {
    eventId: {
      type: String,
      description: "Event id.",
    },
    userType: {
      type: String,
      description: "Either attendee or organizer",
    },
    phoneRequired: {
      type: Boolean,
      description: "Ask for phone number",
      default: false,
    },
  },
  data() {
    return {
      userList: [],
      addUserMode: false,
      addUserFirstName: null,
      addUserLastName: null,
      addUserPhoneNumber: null,
      addUserEmail: null,
      removeUserMode: false,
      removeUserId: null,
    };
  },
  mounted() {
    this.getUsers();
  },
  computed: {
    isAddUserModalValid() {
      return (
        !this.$v.addUserFirstName.$invalid &&
        !this.$v.addUserLastName.$invalid &&
        !this.$v.addUserEmail.$invalid &&
        (!this.$v.addUserPhoneNumber.$invalid || !this.phoneRequired)
      );
    },
    isValidUserFirstNameError() {
      if (this.addUserMode && this.$v.addUserFirstName.$error) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    isValidUserPhoneNumberError() {
      if (this.addUserMode && this.$v.addUserPhoneNumber.$error) {
        return "Must be a valid phone number.";
      }
      return "";
    },
    isValidUserLastNameError() {
      if (this.addUserMode && this.$v.addUserLastName.$error) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    isValidUserEmailError() {
      if (this.addUserMode && this.$v.addUserEmail.$error) {
        return "Please enter a valid email.";
      }
      return "";
    },
  },
  validations: {
    addUserFirstName: {
      required,
      isName: isValidStringWithSpaces,
    },
    addUserLastName: {
      required,
      isName: isValidStringWithSpaces,
    },
    addUserEmail: {
      required,
      email,
    },
    addUserPhoneNumber: {
      phoneValid: isPhone,
    },
  },
  methods: {
    clearUserModalData() {
      this.addUserFirstName = null;
      this.addUserLastName = null;
      this.addUserEmail = null;
      this.addUserPhoneNumber = null;
    },
    addUserSubmit() {
      this.addUserMode = false;
      let data = {
        userDetails: {
          userFirstName: this.addUserFirstName,
          userLastName: this.addUserLastName,
          userEmail: this.addUserEmail,
          userPhoneNumber: this.addUserPhoneNumber,
        },
      };
      axios
        .post(
          "virtual_events/user/virtual_event/" +
            this.eventId +
            "/" +
            this.userType +
            "/add",
          data
        )
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUsers();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    getUsers() {
      axios
        .get(
          "virtual_events/user/virtual_event/" +
            this.eventId +
            "/" +
            this.userType +
            "s/get",
          {}
        )
        .then((res) => {
          this.setUsers(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setUsers(data) {
      this.userList = data[this.userType + "_list"];
    },
    closeRemoveUserModal() {
      this.removeUserMode = false;
    },
    closeAddUserModal() {
      this.addUserMode = false;
      this.clearUserModalData();
      this.$v.$reset();
    },
    openUserModal() {
      this.addUserMode = true;
      this.$v.$reset();
    },
    openRemoveUserModal(userId) {
      this.removeUserId = userId;
      this.removeUserMode = true;
    },
    removeUser() {
      //post to backend
      let userId = this.removeUserId;
      let data = {
        userDetails: {
          userId: userId,
        },
      };
      this.closeRemoveUserModal();
      axios
        .post(
          "virtual_events/user/virtual_event/" +
            this.eventId +
            "/" +
            this.userType +
            "/remove",
          data
        )
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUsers();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
  },
};
</script>
