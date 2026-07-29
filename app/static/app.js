function openModal(status) {
  document.getElementById("modal-status").value = status
  document.getElementById("modal-overlay").classList.remove("hidden")
}

function closeModal() {
  document.getElementById("modal-overlay").classList.add("hidden")
}

let dragged_card = null

let all_cards = document.querySelectorAll(".card")
for (let i = 0; i < all_cards.length; i++) {
  let card = all_cards[i]

  card.addEventListener("dragstart", function () {
    dragged_card = card
    card.classList.add("dragging")
  })

  card.addEventListener("dragend", function () {
    card.classList.remove("dragging")
  })
}

let all_columns = document.querySelectorAll(".column")
for (let i = 0; i < all_columns.length; i++) {
  let column = all_columns[i]

  column.addEventListener("dragover", function (event) {
    event.preventDefault()
  })

  column.addEventListener("drop", function () {
    if (dragged_card == null) {
      return
    }

    let task_id = dragged_card.getAttribute("data-id")
    let new_status = column.getAttribute("data-status")

    fetch("/move-to/" + task_id + "/" + new_status, { method: "POST" })
      .then(function () {
        location.reload()
      })
  })
}

let delete_links = document.querySelectorAll(".delete-link")
for (let i = 0; i < delete_links.length; i++) {
  delete_links[i].addEventListener("click", function (event) {
    let sure = confirm("Delete this task?")
    if (sure == false) {
      event.preventDefault()
    }
  })
}
