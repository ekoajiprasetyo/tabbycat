<template>
  <draggable-item :drag-payload="dragPayload"
                  :hover-panel="true" :hover-panel-item="hoverableData" :hover-panel-type="'team'"
                  :hover-conflicts="true" :hover-conflicts-item="clashableID" :hover-conflicts-type="'team'"
                  :class="[{'bg-dark text-white': isUnavailable}, highlightsCSS, conflictsCSS, hoverConflictsCSS]"
                  :enable-hover="true" :hover-item="hoverableData" :hover-type="hoverableType">

      <span slot="number" class="d-none"><span></span></span>
      <span slot="title" v-text="teamName"></span>
      <span slot="subtitle">
        <span>{{ institutionCode }}</span>
      </span>

  </draggable-item>
</template>

<script>
import { mapState } from 'vuex'
import DraggableItem from '../../templates/allocations/DraggableItem.vue'
import HighlightableMixin from '../../templates/allocations/HighlightableMixin.vue'
import HoverablePanelMixin from '../../templates/allocations/HoverablePanelMixin.vue'
import HoverableConflictReceiverMixin from '../../templates/allocations/HoverableConflictReceiverMixin.vue'

export default {
  mixins: [HoverablePanelMixin, HighlightableMixin, HoverableConflictReceiverMixin],
  components: { DraggableItem },
  props: {
    item: Object,
    dragPayload: Object,
    isTrainee: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    teamName: function () {
      let name = this.item.short_name // Default
      if (this.extra.codeNames === 'everywhere' || this.extra.codeNames === 'admin-tooltips-real') {
        name = this.item.code_name
        if (name === '') {
          name = this.gettext('No code name set')
        }
      }
      return name
    },
    isUnavailable: function () {
      if (this.$store.state.round.stage === 'E') {
        return false // Team availabilities are not set in break rounds so supress the coloring
      }
      return !this.item.available
    },
    highlightData: function () {
      return this.item
    },
    clashableType: function () {
      return 'team'
    },
    clashableID: function () {
      return this.item && this.item.id ? this.item.id : null
    },
    hoverableData: function () {
      return this.item
    },
    hoverableType: function () {
      return 'team'
    },
    institutionCode: function () {
      if (this.item.institution) {
        return this.$store.state.institutions[this.item.institution].code
      } else {
        return this.gettext('Unaffiliated')
      }
    },
    conflictsCSS: function () {
      // Panel-level team-vs-team conflicts within the same debate
      const debateId = this.dragPayload && this.dragPayload.assignment
      if (!debateId || !this.item) { return '' }
      const debate = this.$store.getters.allDebatesOrPanels[debateId]
      if (!debate || !debate.teams) { return '' }

      // Collect other team IDs in this debate
      const otherIds = []
      for (const pos in debate.teams) {
        const tid = debate.teams[pos]
        if (tid !== null && tid !== this.item.id) { otherIds.push(tid) }
      }
      if (otherIds.length === 0) { return '' }

      // Same-institution (orange)
      if (this.item.institution) {
        for (const oid of otherIds) {
          const ot = this.$store.getters.allocatableItems[oid]
          if (ot && ot.institution && ot.institution === this.item.institution) {
            return 'conflictable panel-institution'
          }
        }
      }

      // History (blue shades): pick most recent ago among opponents in this debate
      const histories = this.$store.getters.teamHistoriesForItem(this.item.id)
      if (histories && histories.team) {
        let smallestAgo = 99
        for (const h of histories.team) {
          if (otherIds.includes(h.id) && h.ago < smallestAgo) {
            smallestAgo = h.ago
          }
        }
        if (smallestAgo !== 99) {
          return `conflictable panel-histories-${smallestAgo}-ago`
        }
      }
      return ''
    },
    ...mapState(['extra']),
  },
}
</script>
