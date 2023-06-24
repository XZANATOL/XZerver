let global_selected = new Set()

function checkedItemChecker(element){
	if (element.checked){
		global_selected.add(element.id)
	}else{
		global_selected.delete(element.id)
	}
}
function clearSelections(){
	global_selected.clear()
	let checkboxes = document.querySelectorAll("input[name='selected']")
	checkboxes.forEach(checkbox => {
		checkbox.checked = false
	})
}


async function getSharedFolders(path="") {
	let queryEndpoint = `${location.origin}/${location.pathname}path?path=`

	let locationBar = document.querySelector("input[name='locationbar']")
	let directoryPath = "";

	if(path == ".."){
		directoryPath = locationBar.value.split("/")
		directoryPath.splice(directoryPath.length-2, 2)
		directoryPath = directoryPath.join("/")
	}else{
		directoryPath = `${locationBar.value}${path}`
	}

	if(
		((locationBar.value == "") && (path == "" || path == ".."))
		||
		(path == ".." && directoryPath == "")
	){
		locationBar.value = ""
	}else{
		locationBar.value = `${directoryPath}/`
	}

	queryEndpoint += directoryPath
	let records = await fetch(queryEndpoint, {
		credentials: "same-origin"
	})
	records = await records.json()
	updateExplorer(records.directory)
}


function updateExplorer(records){
	let fileExplorerTable = document.querySelector("tbody")
	fileExplorerTable.innerHTML = ""
	const tableCellCreator = (text) => {
		let td = document.createElement("td")
		let tdDiv = document.createElement("div")
		tdDiv.innerText = text
		td.appendChild(tdDiv)
		return td
	}

	records.forEach( record => {
		let checkboxColumn = document.createElement("td")
		checkbox = document.createElement("input")
		checkbox.type = "checkbox"
		checkbox.name = "selected"
		checkbox.id = record.path
		checkbox.addEventListener("click", (event) => {
			checkedItemChecker(event.target)
			event.stopPropagation() 
		})
		checkboxColumn.appendChild(checkbox)

		const nameColumn = tableCellCreator(record.name)
		const typeColumn = tableCellCreator(record.type)
		const sizeColumn = tableCellCreator(record.size)
		const dtModifiedColumn = tableCellCreator(record.dt_modified)

		const tableRow = document.createElement("tr")
		tableRow.id = record.path
		tableRow.appendChild(checkboxColumn)
		tableRow.appendChild(nameColumn)
		tableRow.appendChild(typeColumn)
		tableRow.appendChild(sizeColumn)
		tableRow.appendChild(dtModifiedColumn)
		tableRow.addEventListener("click", (event) => {
			if(event.detail == 1){
				clearSelections()
				let checkbox = tableRow.querySelector(`input`)
				checkbox.checked = true
				checkedItemChecker(checkbox)
			}else{
				if(event.target.tagName == "TD"){
					if(event.target.parentElement.childNodes[2].innerText == "dir"){
						getSharedFolders(event.target.parentElement.id)
					}else{
						console.log("TD file")
					}		
				}else{
					if(event.target.parentElement.parentElement.childNodes[2].innerText == "dir"){
						getSharedFolders(event.target.parentElement.parentElement.id)
					}else{
						console.log("TD > DIV file")
					}
				}
			}
		})

		fileExplorerTable.appendChild(tableRow)
	})
}


window.onload = async (event) => {
	await getSharedFolders("")
}