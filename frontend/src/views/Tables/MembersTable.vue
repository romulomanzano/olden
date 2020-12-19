<template>
  <div>
    <div class="row align-items-center">
      <div class="col">
        <h6 class="heading-small text-muted mb-4">
          <template v-if="active">
            Active Members
          </template>
          <template v-else>Inactive Members</template>
        </h6>
      </div>
      <div class="col text-right" v-if="active">
        <base-button
          type="primary"
          size="sm"
          v-if="!addUserMode"
          @click="openUserModal"
          >Add Member</base-button
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
          <th>Phone Number</th>
          <th v-if="active"></th>
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

          <th scope="row">
            {{ row.phone_number }}
          </th>

          <td v-if="active" class="text-right">
            <base-button
              type="danger"
              data-toggle="tooltip"
              data-placement="top"
              title="Remove from organization"
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
                <h3>Enter Member Details</h3>
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
            Remove Member
          </h4>
          <p>
            This will mark this member as inactive, you will have to add them
            again.
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
  name: "members-table",
  props: {
    active: {
      type: Boolean,
      description: "Whether to filter for active or inactive members",
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
        !this.$v.addUserPhoneNumber.$invalid
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
        userFirstName: this.addUserFirstName,
        userLastName: this.addUserLastName,
        userEmail: this.addUserEmail,
        userPhoneNumber: this.addUserPhoneNumber,
      };
      axios
        .post(
          "organization/" + this.$store.state.organizationId + "/members/add",
          data
        )
        .then((res) => {
          this.clearUserModalData();
          this.$message.success(res.data.message);
          this.getUsers();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    getUsers() {
      axios
        .get("organization/" + this.$store.state.organizationId + "/members", {
          params: { active: this.active },
        })
        .then((res) => {
          this.setUsers(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setUsers(data) {
      this.userList = data["members"];
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
      this.closeRemoveUserModal();
      axios
        .post(
          "organization/" +
            this.$store.state.organizationId +
            "/members/" +
            this.removeUserId +
            "/archive",
          {}
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
