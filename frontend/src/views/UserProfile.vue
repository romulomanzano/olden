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
                  <h3 class="mb-0">My account</h3>
                </div>
                <div class="col-4 text-right">
                  <base-button
                    type="primary"
                    icon="fa fa-edit"
                    v-if="!editMode"
                    @click="editMode = true"
                    >Edit</base-button
                  >
                  <base-button
                    type="danger"
                    icon="fa fa-stop-circle"
                    v-if="editMode"
                    @click="cancelEdit"
                    >Cancel</base-button
                  >
                  <base-button
                    type="info"
                    icon="fa fa-save"
                    v-if="editMode"
                    @click="submitForm"
                    >Save</base-button
                  >
                </div>
              </div>
            </div>
            <template>
              <form @submit.prevent>
                <h6 class="heading-small text-muted mb-4">
                  Contact information
                </h6>
                <div class="pl-lg-4">
                  <div class="row">
                    <div class="col-lg">
                      <base-input
                        label="First name"
                        placeholder="First name"
                        input-classes="form-control-alternative"
                        v-model="firstName"
                        :disabled="!editMode"
                        :error="firstNameError"
                      />
                    </div>
                    <div class="col-lg">
                      <base-input
                        label="Last name"
                        placeholder="Last name"
                        @blur="$v.lastName.$touch()"
                        input-classes="form-control-alternative"
                        v-model="lastName"
                        :disabled="!editMode"
                        :error="lastNameError"
                      />
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-lg-6">
                      <base-input
                        label="Phone Number"
                        placeholder="8888888888"
                        input-classes="form-control-alternative"
                        v-model="phoneNumber"
                        type="tel"
                        :disabled="!editMode"
                        :error="phoneNumberError"
                        maxlength="10"
                      />
                    </div>
                    <div class="col-lg-6">
                      <base-input
                        label="Email address"
                        placeholder="jesse@example.com"
                        input-classes="form-control-alternative"
                        :disabled="true"
                        v-model="email"
                      />
                    </div>
                  </div>
                </div>
                <hr class="my-4" />
                <!-- Address -->
                <h6 class="heading-small text-muted mb-4">
                  Address information
                </h6>
                <div class="pl-lg-4">
                  <div class="row">
                    <div class="col-md-12">
                      <base-input
                        label="Address"
                        placeholder="Home Address"
                        input-classes="form-control-alternative"
                        v-model="addressLine1"
                        :disabled="!editMode"
                        :error="addressError"
                      />
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-lg-4">
                      <base-input
                        label="City"
                        placeholder="City"
                        input-classes="form-control-alternative"
                        v-model="city"
                        :disabled="!editMode"
                        :error="cityError"
                      />
                    </div>
                    <div class="col-lg-3">
                      <base-input
                        label="Country"
                        placeholder="Country"
                        input-classes="form-control-alternative"
                        v-model="country"
                        :disabled="true"
                      />
                    </div>
                    <div class="col-lg-2">
                      <base-input
                        label="State"
                        placeholder="ST"
                        input-classes="form-control-alternative"
                        v-model="state"
                        :disabled="!editMode"
                        maxlength="2"
                        :error="stateError"
                      />
                    </div>
                    <div class="col-lg-3">
                      <base-input
                        label="Postal code"
                        placeholder="Postal code"
                        input-classes="form-control-alternative"
                        v-model="zipCode"
                        :disabled="!editMode"
                        :error="zipError"
                      />
                    </div>
                  </div>
                </div>
              </form>
            </template>
          </card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { required, minLength } from "vuelidate/lib/validators";
import axios from "../axios-auth";

const isPhone = (value) => /^[0-9]{10}$/.test(value);
const isZip = (value) => /^[0-9]{5}(?:-[0-9]{4})?$/.test(value);
const isValidState = (value, vm) => vm.us_states.includes(value.toUpperCase());
const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);

export default {
  name: "user-profile",
  data() {
    return {
      firstName: "",
      lastName: "",
      addressLine1: "",
      city: "",
      country: "United States",
      zipCode: "",
      phoneNumber: "",
      email: "",
      editMode: false,
      us_states: null,
      state: "",
    };
  },
  mounted() {
    axios
      .get("utils/states/us", {})
      .then((res) => {
        this.us_states = res.data;
      })
      .catch((error) => this.$message.error(error.response.data.message));
    //set address
    this.getUserProfile();
    this.email = this.$store.state.userEmail;
  },
  computed: {
    isFormValid() {
      return (
        !this.$v.phoneNumber.$invalid &&
        !this.$v.zipCode.$invalid &&
        !this.$v.firstName.$invalid &&
        !this.$v.lastName.$invalid &&
        !this.$v.addressLine1.$invalid &&
        !this.$v.city.$invalid &&
        !this.$v.state.$invalid
      );
    },
    firstNameError() {
      if (this.editMode && this.$v.firstName.$invalid) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    lastNameError() {
      if (this.editMode && this.$v.lastName.$invalid) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    phoneNumberError() {
      if (this.editMode && this.$v.phoneNumber.$invalid) {
        return "Please enter a valid phone number.";
      }
      return "";
    },
    zipError() {
      if (this.editMode && this.$v.zipCode.$invalid) {
        return "Please enter a valid five digit zip code.";
      }
      return "";
    },
    cityError() {
      if (this.editMode && this.$v.city.$invalid) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    stateError() {
      if (this.editMode && this.$v.state.$invalid) {
        return "Must enter a valid U.S. state.";
      }
      return "";
    },
    addressError() {
      if (this.editMode && this.$v.addressLine1.$invalid) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
  },
  validations: {
    phoneNumber: {
      required,
      phoneValid: isPhone,
    },
    zipCode: {
      required,
      zipValid: isZip,
    },
    firstName: {
      required,
      isName: isValidStringWithSpaces,
    },
    lastName: {
      required,
      isLastName: isValidStringWithSpaces,
    },
    addressLine1: {
      required,
      minLength: minLength(5),
    },
    city: {
      required,
      isValidCity: isValidStringWithSpaces,
    },
    state: {
      required,
      stateValid: isValidState,
    },
  },
  methods: {
    cancelEdit() {
      this.editMode = false;
      this.getUserProfile();
    },
    submitForm() {
      this.editMode = false;
      let data = {
        address: {
          addressLine1: this.addressLine1,
          zipCode: this.zipCode,
          city: this.city,
          state: this.state,
        },
        personalInfo: {
          firstName: this.firstName,
          lastName: this.lastName,
          phoneNumber: this.phoneNumber,
        },
      };
      axios
        .post("profile/user/profile", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.setProfile(res.data.profile);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    getUserProfile() {
      axios
        .get("profile/user/profile", {})
        .then((res) => {
          this.setProfile(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setProfile(data) {
      let address = data.address;
      this.addressLine1 = address.address_line_1;
      this.city = address.city;
      this.state = address.state;
      this.zipCode = address.zipcode;
      //personal info
      let personalInfo = data.personal_info;
      this.firstName = personalInfo.first_name;
      this.lastName = personalInfo.last_name;
      this.phoneNumber = personalInfo.phone_number;
    },
  },
};
</script>
<style></style>
