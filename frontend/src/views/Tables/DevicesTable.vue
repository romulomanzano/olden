<template>
  <div :class="titleType === 'h3' ? 'card shadow' : ''">
    <div :class="titleType === 'h3' ? 'card-header border-0' : ''">
      <div class="row align-items-center">
        <div class="col">
          <template v-if="titleType === 'h3'">
            <h3 class="mb-0" :class="type === 'dark' ? 'text-white' : ''">
              {{ title }}
            </h3>
          </template>

          <template v-else>
            <h6 class="heading-small text-muted mb-4">
              {{ title }}
            </h6>
          </template>
        </div>
        <div class="col text-right">
          <template v-if="planIdFilter">
            <base-button
              type="secondary"
              size="sm"
              icon="fa fa-link"
              :disabled="!unlinkedDevicesAvailable"
              v-if="!linkDeviceCurrentPlanMode"
              @click="openLinkDeviceModal"
              >Link Existing Device</base-button
            >
          </template>

          <base-button
            type="primary"
            size="sm"
            icon="fa fa-plus"
            v-if="!newDeviceMode"
            @click="openModal"
            >Add New Device</base-button
          >
        </div>
      </div>
    </div>
    <div class="table-responsive">
      <base-table
        class="table align-items-center"
        :class="type === 'dark' ? 'table-dark' : ''"
        :thead-classes="type === 'dark' ? 'thead-dark' : 'thead-light'"
        tbody-classes="list"
        :data="deviceList"
      >
        <template slot="columns">
          <th>Device Alias</th>
          <th>Registered On</th>
          <th>Status</th>
          <th>Pulse Date</th>
          <th>Safety Plan</th>
          <th>Address</th>
          <th></th>
        </template>

        <template slot-scope="{ row }">
          <th scope="row">
            {{ row.device_registration.device_alias }}
          </th>
          <td class="budget" v-if="row.device_registration">
            {{
              new Date(row.device_registration.registration_date.$date)
                | moment("dddd, MMMM Do YYYY")
            }}
          </td>
          <td v-else>
            N/A
          </td>
          <td>
            {{ row.status | capitalize }}
          </td>
          <td v-if="row.pulse_date">
            {{ row.pulse_date.$date | moment("dddd, MMMM Do YYYY") }}
          </td>
          <td v-else>
            N/A
          </td>
          <td>
            {{ (row.device_registration.safety_plan || {}).name }}
          </td>
          <template v-if="row.device_registration.registration_address">
            <td>
              {{ row.device_registration.registration_address.address_line_1 }}
              ...
            </td>
          </template>

          <template v-else>
            <td></td>
          </template>

          <td class="text-right">
            <div :style="{ height: '100%' }">
              <base-dropdown
                direction="down"
                :hideArrow="true"
                position="right"
                class="nav-link pr-0"
              >
                <base-button
                  slot="title"
                  type="secondary"
                  size="sm"
                  icon="fa fa-ellipsis-v"
                ></base-button>
                <div :style="{ height: '100%' }">
                  <a
                    class="dropdown-item"
                    @click="
                      openRegistrationAddressModal(
                        row._id.$oid,
                        row.device_registration.registration_address,
                        row.device_registration._id.$oid
                      )
                    "
                    >Edit Address</a
                  >
                  <template v-if="!row.device_registration.safety_plan">
                    <a
                      class="dropdown-item"
                      @click="linkToPlanMode(row._id.$oid)"
                      >Link to Plan</a
                    >
                    <a
                      class="dropdown-item"
                      @click="deregisterMode(row._id.$oid)"
                      >Remove</a
                    >
                  </template>
                  <template v-else>
                    <a
                      class="dropdown-item"
                      @click="setUnlinkFromPlanMode(row._id.$oid)"
                      >Unlink from Plan</a
                    >
                  </template>
                </div>
              </base-dropdown>
            </div>
          </td>
        </template>
      </base-table>

      <modal
        :show.sync="newDeviceMode"
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
              <h3>Enter device details</h3>
            </div>
            <form role="form">
              <base-input
                alternative
                class="mb-3"
                v-model="newDeviceAlias"
                placeholder="Device Alias"
                addon-left-icon="ni ni-app"
                @blur="$v.newDeviceAlias.$touch()"
                :error="isValidDeviceAliasError"
              >
              </base-input>
              <base-input
                alternative
                type="text"
                v-model="newDeviceId"
                placeholder="Device Id"
                @blur="$v.newDeviceId.$touch()"
                addon-left-icon="fa fa-barcode"
                :error="isValidDeviceIdError"
              >
              </base-input>
              <template v-if="safetyPlanList">
                <base-input
                  class="mb-3"
                  addon-left-icon="fa fa-life-ring"
                  :required="false"
                >
                  <select class="form-control" v-model="newDeviceSafetyPlan">
                    <option
                      v-for="option in safetyPlanList"
                      :value="option"
                      :key="option._id.$oid"
                      >Safety Plan: {{ option.name }}</option
                    >
                  </select>
                </base-input>
              </template>

              <div class="text-center">
                <base-button type="danger" class="my-4" @click="closeModal"
                  >Cancel</base-button
                >
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="!isModalFormValid"
                  @click="submitNewDevice"
                  >Submit</base-button
                >
              </div>
            </form>
          </template>
        </card>
      </modal>
      <modal
        :show.sync="deleteDeviceMode"
        gradient="primary"
        modal-classes="modal-primary modal-dialog-centered"
      >
        <div class="py-3 text-center">
          <i class="ni ni-bell-55 ni-3x"></i>
          <h4 class="heading mt-4">REMOVE DEVICE</h4>
          <p>
            This will remove this device from your account, you will no longer
            monitor potential falls using this device.
          </p>
        </div>

        <template slot="footer">
          <base-button
            type="link"
            text-color="white"
            class="mr-auto"
            @click="closeDeregisterModal"
          >
            Cancel
          </base-button>
          <base-button class="ml-auto" type="white" @click="deregisterDevice"
            >Deregister anyways</base-button
          >
        </template>
      </modal>

      <modal
        :show.sync="unlinkDeviceMode"
        gradient="primary"
        modal-classes="modal-primary modal-dialog-centered"
      >
        <div class="py-3 text-center">
          <i class="ni ni-bell-55 ni-3x"></i>
          <h4 class="heading mt-4">UNLINK DEVICE</h4>
          <p>
            This will unlink this device from the existing plan, you will no
            longer monitor potential falls using this device.
          </p>
        </div>

        <template slot="footer">
          <base-button
            type="link"
            text-color="white"
            class="mr-auto"
            @click="closeUnlinkModal"
          >
            Cancel
          </base-button>
          <base-button
            class="ml-auto"
            type="white"
            @click="submitUnlinkDeviceFromPlan"
            >Unlink anyways</base-button
          >
        </template>
      </modal>

      <modal
        :show.sync="linkDeviceMode"
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
              <h3>Link to Safety Plan</h3>
            </div>
            <form role="form">
              <div>
                <base-input>
                  <select class="form-control" v-model="linkDeviceSafetyPlan">
                    <option
                      v-for="option in safetyPlanList"
                      :value="option"
                      :key="option._id.$oid"
                      >{{ option.name }}</option
                    >
                  </select>
                </base-input>
              </div>
              <div class="text-center">
                <base-button type="danger" class="my-4" @click="closeLinkModal"
                  >Cancel</base-button
                >
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="linkDeviceSafetyPlan === null"
                  @click="submitLinkDeviceToPlan"
                  >Submit</base-button
                >
              </div>
            </form>
          </template>
        </card>
      </modal>
      <modal
        :show.sync="linkDeviceCurrentPlanMode"
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
              <h3>Link Device To This Plan</h3>
            </div>
            <form role="form">
              <div>
                <base-input>
                  <select class="form-control" v-model="unlinkedDevice">
                    <option
                      v-for="option in unlinkedDeviceList"
                      :value="option"
                      :key="option._id.$oid"
                      >{{ option.device_registration.device_alias }}</option
                    >
                  </select>
                </base-input>
              </div>
              <div class="text-center">
                <base-button
                  type="danger"
                  class="my-4"
                  @click="closeLinkDeviceCurrentPlanModal"
                  >Cancel</base-button
                >
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="unlinkedDevice === null"
                  @click="submitLinkDeviceToCurrentPlan"
                  >Submit</base-button
                >
              </div>
            </form>
          </template>
        </card>
      </modal>
      <modal
        :show.sync="editRegisteredAddressMode"
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
              <h3>Edit Device Address</h3>
            </div>
            <form role="form">
              <div>
                <base-input
                  label="Address"
                  placeholder="Home Address"
                  input-classes="form-control-alternative"
                  v-model="editRegisteredAddress.addressLine1"
                  @blur="$v.editRegisteredAddress.addressLine1.$touch()"
                  :error="addressError"
                />
                <base-input
                  label="City"
                  placeholder="City"
                  input-classes="form-control-alternative"
                  v-model="editRegisteredAddress.city"
                  @blur="$v.editRegisteredAddress.city.$touch()"
                  :error="cityError"
                />
                <base-input label="State">
                  <select
                    class="form-control"
                    v-model="editRegisteredAddress.state"
                  >
                    <option
                      v-for="option in us_states"
                      :value="option"
                      :key="option"
                      >{{ option }}</option
                    >
                  </select>
                </base-input>

                <base-input
                  label="Postal code"
                  placeholder="Postal code"
                  input-classes="form-control-alternative"
                  v-model="editRegisteredAddress.zipCode"
                  @blur="$v.editRegisteredAddress.zipCode.$touch()"
                  :error="zipError"
                />
                <base-input
                  label="Country"
                  placeholder="Country"
                  input-classes="form-control-alternative"
                  v-model="editRegisteredAddress.country"
                  @blur="$v.editRegisteredAddress.country.$touch()"
                  :disabled="true"
                  :error="countryError"
                />
                <base-input
                  label="Land Line Phone Number"
                  placeholder="8888888888"
                  input-classes="form-control-alternative"
                  v-model="editRegisteredAddress.landLineNumber"
                  @blur="$v.editRegisteredAddress.landLineNumber.$touch()"
                  type="tel"
                  :error="phoneError"
                  maxlength="10"
                />
              </div>
              <div class="text-center">
                <base-button
                  type="danger"
                  class="my-4"
                  @click="closeRegistrationAddressModal"
                  >Cancel</base-button
                >
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="!isEditAddressFormValid"
                  @click="submitRegistrationAddress"
                  >Submit</base-button
                >
              </div>
            </form>
          </template>
        </card>
      </modal>
      <!--needed to support dropdown-->
      <div :style="{ height: '120px' }"></div>
    </div>
  </div>
</template>
<script>
import { required, alphaNum, minLength } from "vuelidate/lib/validators";
import axios from "../../axios-auth";

const isZip = (value) => /^[0-9]{5}(?:-[0-9]{4})?$/.test(value);
const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);
const isPhone = (value) =>
  /^[0-9]{10}$/.test(value) || value === null || value === "";

export default {
  name: "devices-table",
  data() {
    return {
      deviceList: [],
      us_states: null,
      newDeviceId: null,
      newDeviceAlias: null,
      newDeviceMode: false,
      newDeviceSafetyPlan: null,
      deleteDeviceMode: false,
      deleteDeviceId: null,
      linkDeviceMode: false,
      linkDeviceSafetyPlan: null,
      linkDeviceId: null,
      safetyPlanList: [],
      unlinkDeviceMode: false,
      unlinkDeviceId: null,
      linkDeviceCurrentPlanMode: false,
      unlinkedDeviceList: [],
      unlinkedDevice: null,
      editRegisteredAddressDeviceId: null,
      editRegisteredAddressDeviceRegistrationId: null,
      editRegisteredAddress: {},
      editRegisteredAddressMode: false,
    };
  },
  props: {
    type: {
      type: String,
    },
    title: String,
    titleType: String,
    planIdFilter: String,
  },
  mounted() {
    axios
      .get("utils/states/us", {})
      .then((res) => {
        this.us_states = res.data;
      })
      .catch((error) => this.$message.error(error.response.data.message));
    this.getUserDevices();
    this.getUnlinkedUserDevices();
    this.getUserSafetyPlans();
  },
  validations: {
    newDeviceAlias: {
      required,
      minLength: minLength(5),
    },
    newDeviceId: {
      required,
      alphaNum,
      minLength: minLength(5),
    },
    editRegisteredAddress: {
      zipCode: {
        required,
        zipValid: isZip,
      },
      addressLine1: {
        required,
        minLength: minLength(5),
      },
      city: {
        required,
        isValidCity: isValidStringWithSpaces,
      },
      country: {
        required,
        isValidCountry: isValidStringWithSpaces,
      },
      landLineNumber: {
        phoneValid: isPhone,
      },
    },
  },
  computed: {
    isEditAddressFormValid() {
      return (
        !this.$v.editRegisteredAddress.zipCode.$invalid &&
        !this.$v.editRegisteredAddress.addressLine1.$invalid &&
        !this.$v.editRegisteredAddress.city.$invalid &&
        !this.$v.editRegisteredAddress.country.$invalid &&
        !(
          this.$v.editRegisteredAddress.landLineNumber &&
          this.$v.editRegisteredAddress.landLineNumber.$invalid
        ) &&
        this.editRegisteredAddress.state
      );
    },
    zipError() {
      if (
        this.editRegisteredAddressMode &&
        this.$v.editRegisteredAddress.zipCode.$error
      ) {
        return "Please enter a valid five digit zip code.";
      }
      return "";
    },
    phoneError() {
      if (
        this.editRegisteredAddressMode &&
        this.$v.editRegisteredAddress.landLineNumber &&
        this.$v.editRegisteredAddress.landLineNumber.$error
      ) {
        return "Please enter a valid number.";
      }
      return "";
    },
    cityError() {
      if (
        this.editRegisteredAddressMode &&
        this.$v.editRegisteredAddress.city.$error
      ) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    countryError() {
      if (
        this.editRegisteredAddressMode &&
        this.$v.editRegisteredAddress.country.$error
      ) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    stateError() {
      if (
        this.editRegisteredAddressMode &&
        this.$v.editRegisteredAddress.state.$error
      ) {
        return "Must enter a valid U.S. state.";
      }
      return "";
    },
    addressError() {
      if (
        this.editRegisteredAddressMode &&
        this.$v.editRegisteredAddress.addressLine1.$error
      ) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
    isModalFormValid() {
      return !this.$v.newDeviceAlias.$invalid && !this.$v.newDeviceId.$invalid;
    },
    isValidDeviceIdError() {
      if (this.newDeviceMode && this.$v.newDeviceId.$error) {
        return "Must not be empty and contain at least 5 alphanumeric characters.";
      }
      return "";
    },
    isValidDeviceAliasError() {
      if (this.newDeviceMode && this.$v.newDeviceAlias.$error) {
        return "Must not be empty and contain at least 5 characters.";
      }
      return "";
    },
    unlinkedDevicesAvailable() {
      return Object.entries(this.unlinkedDeviceList).length > 0;
    },
  },
  methods: {
    openRegistrationAddressModal(deviceId, address, registrationId) {
      this.editRegisteredAddressDeviceId = deviceId;
      this.editRegisteredAddressDeviceRegistrationId = registrationId;
      let addressData = address || { country: "US" };
      this.editRegisteredAddress = {
        _id: addressData._id,
        addressLine1: addressData.address_line_1,
        state: addressData.state,
        zipCode: addressData.zipcode,
        city: addressData.city,
        country: addressData.country,
        landLineNumber: addressData.land_line_number,
      };
      this.editRegisteredAddressMode = true;
      this.$v.$reset();
    },
    closeRegistrationAddressModal() {
      this.editRegisteredAddressDeviceId = null;
      this.editRegisteredAddressDeviceRegistrationId = null;
      this.editRegisteredAddress = {};
      this.editRegisteredAddressMode = false;
      this.$v.$reset();
    },
    submitLinkDeviceToPlan() {
      let data = {
        deviceId: this.linkDeviceId,
        planId: this.linkDeviceSafetyPlan._id.$oid,
      };
      this.closeLinkModal();
      axios
        .post("device/safety_plan/link", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUserDevices();
          this.getUnlinkedUserDevices();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    submitRegistrationAddress() {
      let data = {
        deviceId: this.editRegisteredAddressDeviceId,
        deviceRegistrationId: this.editRegisteredAddressDeviceRegistrationId,
        address: this.editRegisteredAddress,
      };
      this.closeRegistrationAddressModal();
      axios
        .post("device/registration/address/update", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUserDevices();
          this.getUnlinkedUserDevices();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    submitLinkDeviceToCurrentPlan() {
      let data = {
        deviceId: this.unlinkedDevice._id.$oid,
        planId: this.planIdFilter,
      };
      this.closeLinkDeviceCurrentPlanModal();
      axios
        .post("device/safety_plan/link", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUserDevices();
          this.getUnlinkedUserDevices();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    submitUnlinkDeviceFromPlan() {
      let data = {
        deviceId: this.unlinkDeviceId,
      };
      this.closeUnlinkModal();
      axios
        .post("device/safety_plan/unlink", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUserDevices();
          this.getUnlinkedUserDevices();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    getUserSafetyPlans() {
      axios
        .get("safety/user/safety_plans", {})
        .then((res) => {
          this.setSafetyPlans(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setSafetyPlans(data) {
      this.safetyPlanList = data;
    },
    closeLinkDeviceCurrentPlanModal() {
      (this.unlinkedDevice = null), (this.linkDeviceCurrentPlanMode = false);
    },
    closeLinkModal() {
      this.linkDeviceMode = false;
      this.linkDeviceSafetyPlan = null;
      this.linkDeviceId = null;
    },
    closeUnlinkModal() {
      this.unlinkDeviceMode = false;
      this.unlinkDeviceId = null;
    },
    linkToPlanMode(deviceId) {
      this.linkDeviceMode = true;
      this.linkDeviceId = deviceId;
    },
    setUnlinkFromPlanMode(deviceId) {
      this.unlinkDeviceMode = true;
      this.unlinkDeviceId = deviceId;
    },

    getUserDevices() {
      let data = { planIdFilter: this.planIdFilter };
      axios
        .get("device/user/devices", { params: data })
        .then((res) => {
          this.setDevices(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    getUnlinkedUserDevices() {
      let data = { unlinkedFlag: true };
      axios
        .get("device/user/devices", { params: data })
        .then((res) => {
          this.setUnlinkedDevices(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setDevices(data) {
      this.deviceList = data;
    },
    setUnlinkedDevices(data) {
      this.unlinkedDeviceList = data;
    },
    closeModal() {
      this.newDeviceMode = false;
      this.newDeviceAlias = null;
      this.newDeviceId = null;
      this.newDeviceSafetyPlan = null;
    },
    openModal() {
      this.newDeviceMode = true;
      this.$v.$reset();
    },
    openLinkDeviceModal() {
      this.linkDeviceCurrentPlanMode = true;
      this.getUnlinkedUserDevices();
    },
    submitNewDevice() {
      //post to backend
      let data = {
        deviceId: this.newDeviceId,
        deviceAlias: this.newDeviceAlias,
        devicePlanId: this.newDeviceSafetyPlan
          ? this.newDeviceSafetyPlan._id.$oid
          : null,
      };
      this.closeModal();
      axios
        .post("device/user/add", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUserDevices();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    deregisterMode(deviceId) {
      this.deleteDeviceId = deviceId;
      this.deleteDeviceMode = true;
    },
    closeDeregisterModal() {
      this.deleteDeviceMode = false;
      this.deleteDeviceId = null;
    },
    deregisterDevice() {
      //post to backend
      let deviceId = this.deleteDeviceId;
      this.closeDeregisterModal();
      axios
        .post("device/user/deregister/" + deviceId, {})
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUserDevices();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
  },
};
</script>
