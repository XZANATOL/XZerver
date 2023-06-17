let checked_items = []

function deleteItems(){
	let error = false
	checked_items.forEach( async (item, index) => {
		let response = await fetch(`${location.href}${item}/delete`, {
			method: "DELETE",
			headers: {
				"X-CSRFToken": csrf_token
			}
		})
		response = await response.json()
		if (response.status !== 200){
			console.log(response)
			error = true
		}

		if (index == checked_items.length - 1 && error == false){
			location.reload()
		}
	})
}

function checkedItemChecker(element){
	if (element.checked){
		checked_items.push(element.id)
	}else{
		index = checked_items.indexOf(element.id)
		if (index !== -1) {
			checked_items.splice(index, 1);
		}
	}
}

function addEventListiners() {
	let elements = document.querySelectorAll("input[name='selected']")
	elements.forEach( element => {
		element.addEventListener("input", (event) => { checkedItemChecker(element) })
	})

	let deleteButton = document.querySelector("div[class='tool-bar']").querySelectorAll("button").item(1)
	deleteButton.addEventListener("click", (event) => { deleteItems() })
}

addEventListiners()