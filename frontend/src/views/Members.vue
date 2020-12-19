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
                  <h3 class="mb-0">Members</h3>
                </div>
              </div>
            </div>
            <template>
              <form @submit.prevent>
                <tabs>
                  <tab-pane title="Active Members">
                    <div class="col">
                      <members-table
                        :active="true"
                        ref="activeMembers"
                      ></members-table>
                    </div>
                  </tab-pane>
                  <tab-pane title="Inactive Members">
                    <div class="col">
                      <members-table
                        :active="false"
                        ref="inactiveMembers"
                      ></members-table>
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
import MembersTable from "./Tables/MembersTable";

export default {
  name: "virtual-event-form",
  components: {
    MembersTable,
  },
  data() {
    return {};
  },
};
</script>
<style></style>
