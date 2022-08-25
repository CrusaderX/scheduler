<template>
  <form @submit.prevent="onSubmit" class="bg-white dark:bg-dark-grey rounded-lg p-1">
    <div class="p-5 pr-3 flex flex-col gap-6 max-h-[90vh] overflow-y-scroll">
      <div class="flex justify-between items-center">
        <h4 class="text-black dark:text-white font-bold text-lg">
          {{ managerStore.boardForm.edit ? 'Edit Board' : 'Add New Board' }}
        </h4>
      </div>
      <BaseInput ref="inputTitle" v-model="board.name" inputName="Board Name" placeholder="Default" />
      <div class="flex flex-col gap-3">
        <p class="text-medium-grey dark:text-white text-xs font-bold">Board Columns</p>
        <div class="flex items-center justify-between gap-4" v-for="(column, index) in board.columns" :key="index">
          <BaseInput :ref="el => { inputs[index] = el }" v-model="column.name"
            :placeholder="columnsPlaceholders[index] ? columnsPlaceholders[index] : 'Default'" />
          <IconCross @click="deleteColumn(index)" class="cursor-pointer" />
        </div>
        <ButtonSecondaryLarge @click.stop="addColumn">+ Add new column</ButtonSecondaryLarge>
      </div>
      <ButtonPrimaryLarge type="submit">
        {{ managerStore.boardForm.edit ? 'Save Changes' : 'Create New Board' }}
      </ButtonPrimaryLarge>
    </div>
  </form>
</template>

<script setup>

import { ref, reactive, onBeforeUpdate } from 'vue'
import { useBoardsStore } from '@/stores/boards.js';
import { useManagerStore } from '@/stores/manager.js';
import BaseInput from '@/components/form/BaseInput.vue';
import IconCross from '@/components/icons/IconCross.vue';
import ButtonPrimaryLarge from '@/components/buttons/PrimaryLarge.vue';
import ButtonSecondaryLarge from '@/components/buttons/SecondaryLarge.vue';

const boardsStore = useBoardsStore();
const managerStore = useManagerStore();

const inputTitle = ref(null)
const inputs = ref([])

const board = reactive({
  name: '',
  columns: []
})
const columnsPlaceholders = {
  0: '',
  1: '',
  2: ''
}
const deleteColumn = (index) => {
  if (board.columns.length === 2) {
    board.columns[index].name = ''
    board.columns[index].tasks = [{ name: '', tasks: [] }]
  } else {
    board.columns.splice(index, 1)
  }
}
const addColumn = () => {
  board.columns.push({ name: '', tasks: [] })
}
const onSubmit = () => {
  if (managerStore.boardForm.edit) {
    boardsStore.board = board
    managerStore.hideOverlay()
  }
}

//EDIT MODE
if (managerStore.boardForm.edit) {
  board.name = JSON.parse(JSON.stringify(boardsStore.board.name))
  board.columns = JSON.parse(JSON.stringify(boardsStore.getCurrentBoard.columns))
} else {
  board.columns = [{ name: '', tasks: [] }, { name: '', tasks: [] }]
}
onBeforeUpdate(() => {
  inputs.value = []
})
</script>
