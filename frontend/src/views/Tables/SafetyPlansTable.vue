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
          v-if="!modalSafetyPlanMode"
          @click="openModal"
          >Add Safety Plan</base-button
        >
      </div>
    </div>
    <div>
      <modal
        :show.sync="modalSafetyPlanMode"
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
              <h3>Enter Safety Plan details</h3>
            </div>
            <form role="form">
              <base-input
                alternative
                class="mb-3"
                v-model="modalSafetyPlanName"
                placeholder="Safety Plan Name"
                @blur="$v.modalSafetyPlanName.$touch()"
                :error="isValidPlanNameError"
              >
              </base-input>

              <div class="text-center">
                <base-button type="danger" class="my-4" @click="closeModal"
                  >Cancel</base-button
                >
                <base-button
                  type="primary"
                  class="my-4"
                  :disabled="!isModalFormValid"
                  @click="submitSafetyPlan"
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
        :data="safetyPlanList"
      >
        <template slot="columns">
          <th>Plan Name</th>
          <th></th>
        </template>

        <template slot-scope="{ row }">
          <th scope="row">
            {{ row.name | capitalize }}
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
        :show.sync="archiveSafetyPlanMode"
        gradient="primary"
        modal-classes="modal-primary modal-dialog-centered"
      >
        <div class="py-3 text-center">
          <i class="ni ni-bell-55 ni-3x"></i>
          <h4 class="heading mt-4">Archive Safety Plan</h4>
          <p>
            This will archive this plan, we will no longer be able to alert the
            caring members.
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
          <base-button class="ml-auto" type="white" @click="archiveSafetyPlan"
            >Archive anyways</base-button
          >
        </template>
      </modal>
    </div>
  </div>
</template>
<script>
import axios from "../../axios-auth";
import { required } from "vuelidate/lib/validators";

const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);

export default {
  name: "safety-plans-table",
  props: {
    type: {
      type: String,
    },
    title: String,
  },
  mounted() {
    this.getUserSafetyPlans();
  },
  data() {
    return {
      safetyPlanList: [],
      modalSafetyPlanName: null,
      modalSafetyPlanMode: null,
      archiveSafetyPlanMode: false,
      archiveSafetyPlanId: null,
      recipientList: null,
    };
  },
  validations: {
    modalSafetyPlanName: {
      required,
      isName: isValidStringWithSpaces,
    },
  },
  computed: {
    isModalFormValid() {
      return !this.$v.modalSafetyPlanName.$invalid;
    },
    isValidPlanNameError() {
      if (this.modalSafetyPlanMode && this.$v.modalSafetyPlanName.$error) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
  },
  methods: {
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
    closeModal() {
      this.modalSafetyPlanMode = false;
      this.modalSafetyPlanName = null;
    },
    openModal() {
      this.modalSafetyPlanMode = true;
      this.$v.$reset();
    },
    submitSafetyPlan() {
      //post to backend
      let data = {
        modalSafetyPlanName: this.modalSafetyPlanName,
      };
      this.closeModal();
      //depending of the value either post new or update safety plan
      axios
        .post("safety/user/safety_plan/add", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.$router.push("safety_plan?id=" + res.data.plan._id.$oid);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    archiveMode(safetyId) {
      this.archiveSafetyPlanId = safetyId;
      this.archiveSafetyPlanMode = true;
    },
    editMode(row) {
      this.$v.$reset();
      //set to pre-existing values
      this.$router.push("safety_plan?id=" + row._id.$oid);
    },
    closeDeregisterModal() {
      this.archiveSafetyPlanMode = false;
    },
    archiveSafetyPlan() {
      //post to backend
      let planId = this.archiveSafetyPlanId;
      this.closeDeregisterModal();
      axios
        .post("safety/user/safety_plan/" + planId + "/archive", {})
        .then((res) => {
          this.$message.success(res.data.message);
          this.getUserSafetyPlans();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
  },
};
</script>
