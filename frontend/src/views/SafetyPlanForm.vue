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
                  <h3 class="mb-0">{{ planName }}</h3>
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
                    title="Edit Plan Name"
                    @click="openForm"
                  >
                  </base-button>
                </div>
              </div>
            </div>
            <template>
              <form @submit.prevent>
                <tabs>
                  <tab-pane title="Recipients">
                    <div class="col">
                      <safety-plan-user-table
                        :planId="planId"
                        userType="recipient"
                      ></safety-plan-user-table>
                    </div>
                  </tab-pane>
                  <tab-pane title="Caregivers">
                    <div class="col">
                      <safety-plan-user-table
                        :planId="planId"
                        userType="caregiver"
                        :phoneRequired="true"
                      ></safety-plan-user-table>
                    </div>
                  </tab-pane>
                  <tab-pane title="Devices">
                    <div class="col">
                      <devices-table
                        title="Registered Devices"
                        titleType="h6"
                        :planIdFilter="planId"
                      ></devices-table>
                    </div>
                  </tab-pane>
                  <tab-pane title="Alert Settings">
                    <div class="col">
                      <alert-settings-table
                        :planId="planId"
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
                      <h3>New Plan Name</h3>
                    </div>
                    <form role="form">
                      <base-input
                        alternative
                        class="mb-3"
                        v-model="editPlanName"
                        @blur="$v.editPlanName.$touch()"
                        :error="planNameError"
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
import SafetyPlanUserTable from "./Tables/SafetyPlanUserTable";
import DevicesTable from "./Tables/DevicesTable";
import AlertSettingsTable from "./Tables/AlertSettingsTable";

const isValidStringWithSpaces = (value) => /^[a-zA-Z\s]*$/.test(value);

export default {
  name: "safety-plan-form",
  components: {
    SafetyPlanUserTable,
    DevicesTable,
    AlertSettingsTable,
  },

  data() {
    return {
      planName: "",
      planId: null,
      editMode: false,
      editPlanName: null,
    };
  },
  beforeMount() {
    if (this.$route.query.id) {
      this.planId = this.$route.query.id;
      this.getSafetyPlan();
    } else {
      this.$router.push("safety_plans");
    }
  },
  computed: {
    isFormValid() {
      return !this.$v.editPlanName.$invalid;
    },
    planNameError() {
      if (this.editMode && this.$v.editPlanName.$error) {
        return "Must not be empty and only contain letters.";
      }
      return "";
    },
  },
  validations: {
    editPlanName: {
      required,
      isName: isValidStringWithSpaces,
    },
  },
  methods: {
    cancelEdit() {
      this.editMode = false;
      this.$v.$reset();
      this.editPlanName = "";
    },
    openForm() {
      this.editPlanName = "";
      this.$v.$reset();
      this.editMode = true;
    },
    submitForm() {
      this.editMode = false;
      let data = {
        planInfo: {
          name: this.editPlanName,
        },
      };
      axios
        .post("safety/user/safety_plan/" + this.planId + "/update", data)
        .then((res) => {
          this.$message.success(res.data.message);
          this.getSafetyPlan();
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    getSafetyPlan() {
      axios
        .get("safety/user/safety_plan/" + this.planId, {})
        .then((res) => {
          this.setPlan(res.data);
        })
        .catch((error) => this.$message.error(error.response.data.message));
    },
    setPlan(data) {
      //personal info
      let planInfo = data.plan;
      this.planName = planInfo.name;
      this.planId = planInfo._id.$oid;
    },
  },
};
</script>
<style></style>
