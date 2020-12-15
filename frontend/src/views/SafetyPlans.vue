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
                  <h3 class="mb-0">Safety Plans</h3>
                </div>
              </div>
            </div>
            <template>
              <form @submit.prevent>
                <tabs>
                  <tab-pane title="Plans">
                    <div class="col">
                      <safety-plans-table title="Active Plans">
                      </safety-plans-table>
                    </div>
                  </tab-pane>
                  <tab-pane title="Devices">
                    <div class="col">
                      <devices-table
                        title="Registered Devices"
                        titleType="h6"
                      ></devices-table>
                    </div>
                  </tab-pane>
                </tabs>
              </form>
            </template>
          </card>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import SafetyPlansTable from "./Tables/SafetyPlansTable.vue";
import DevicesTable from "./Tables/DevicesTable";

export default {
  name: "safety-plans",
  components: {
    SafetyPlansTable,
    DevicesTable,
  },
};
</script>
<style></style>
