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


async function getSharedItems(path="") {
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
		if(path == ""){
			locationBar.value = `${directoryPath}`
		}else{
			locationBar.value = `${directoryPath}/`
		}
	}

	queryEndpoint += directoryPath
	let records = await fetch(queryEndpoint, {
		credentials: "same-origin"
	})
	.then(res => {
		return res.json()
	})
	.catch(err => {
		notifyCardFactory(`Error: ${err}`)
	})

	updateExplorer(records.directory, records.stats)
	uploaderUpdater(records.write_access)
}


function getFile(filename){
	let queryEndpoint = `${location.origin}${location.pathname}download?path=`
	const locationBar = document.querySelector("input[name='locationbar']").value
	queryEndpoint += `${locationBar}${filename}`
	const link = document.createElement("a")
	link.href = queryEndpoint
	link.target = "_blank"
	link.click()
}


function updateExplorer(records, stats){
	let fileExplorerTable = document.querySelector("tbody")
	let pathProperties = document.querySelector("#properties")
	let folderCount = 0
	let fileCount = 0
	fileExplorerTable.innerHTML = ""
	const tableCellCreator = (text) => {
		let td = document.createElement("td")
		let tdDiv = document.createElement("div")
		tdDiv.innerText = text
		td.appendChild(tdDiv)
		return td
	}

	records.forEach( record => {
		if(record.type == "dir"){
			folderCount += 1
		}else{
			fileCount += 1
		}

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
						getSharedItems(event.target.parentElement.id)
					}else{
						getFile(event.target.parentElement.childNodes[1].innerText)
					}		
				}else{
					if(event.target.parentElement.parentElement.childNodes[2].innerText == "dir"){
						getSharedItems(event.target.parentElement.parentElement.id)
					}else{
						getFile(event.target.parentElement.parentElement.childNodes[1].innerText)
					}
				}
			}
		})

		fileExplorerTable.appendChild(tableRow)
	})

	let folderCountLi = document.createElement("li")
	let fileCountLi = document.createElement("li")
	let usedSpaceLi = document.createElement("li")
	let freeSpaceLi = document.createElement("li")
	folderCountLi.innerText = `${folderCount} Folders`
	fileCountLi.innerText = `${fileCount} Files`
	usedSpaceLi.innerText = `Used: ${stats.usedspace} GB`
	freeSpaceLi.innerText = `Free: ${stats.freespace} GB`
	pathProperties.innerHTML = ""
	pathProperties.appendChild(folderCountLi)
	pathProperties.appendChild(fileCountLi)
	pathProperties.appendChild(usedSpaceLi)
	pathProperties.appendChild(freeSpaceLi)
}


function uploaderUpdater(access){
	let uploadSection = document.querySelector(".upload")
	if(access){
		uploadSection.classList.remove("hidden")
	}else{
		if(!uploadSection.classList.contains("hidden")){
			uploadSection.classList.add("hidden")
		}
	}
}


function notifyCardFactory(text){
	let notifyPanel = document.querySelector(".notfi")
	let notifyCard = document.createElement("div")
	notifyCard.classList.add("notfi-item")

	let notifyDeleteButton = document.createElement("button")
	notifyDeleteButton.classList.add("notfi-item-del")
	notifyDeleteButton.innerText = "X"
	notifyDeleteButton.addEventListener("click", (e) => {
		e.target.parentElement.remove()
	})

	let notifySpan = document.createElement("span")
	notifySpan.classList.add("notfi-item-span")
	notifySpan.innerText = text

	notifyCard.appendChild(notifyDeleteButton)
	notifyCard.appendChild(notifySpan)
	notifyPanel.appendChild(notifyCard)
	return notifyCard
}


async function uploadItems() {
	const uploadEndpoints = `${location.origin}/${location.pathname}`
	const uploadInput = document.querySelector("#uploadinput").files
	const locationBar = document.querySelector("input[name='locationbar']").value

	let checkWriteAccess = await fetch(`${uploadEndpoints}has_write_access?path=${locationBar}`, {
		credentials: "same-origin"
	})
	.then(res => {
		return res.json()
	})
	.catch(err => {
		notifyCardFactory(`Error: ${err}`)
	})

	if (!checkWriteAccess.access){
		notifyCardFactory("You don't have write access to this directory")
	}
	else{

		const asyncXHR = (file) => {
			return new Promise((resolve, reject) => {
				let card = notifyCardFactory(`Uploading file: ${file.name}`)
				let button = card.querySelector("button")
				let sendFile = new XMLHttpRequest()
				sendFile.open("POST", `${uploadEndpoints}upload?path=${locationBar}`, true)
				sendFile.setRequestHeader("credentials", "same-origin")
				sendFile.onload = () => {
					getSharedItems("")
				}
				sendFile.onerror = () => {
					console.error(sendFile.statusText)
				}
				sendFile.upload.onprogress = e => {
					if(e.lengthComputable){
						card.querySelector("span").innerText = `Sending file: ${file.name}\n${Math.round(e.loaded / 1_000_000, 2)} / ${Math.round(e.total / 1_000_000, 2)} MB`
					}
				}
				const formData = new FormData();
				formData.append('file', file);
				button.addEventListener("click", (e) => {
					sendFile.abort()	
				})
				
				sendFile.send(formData)
			})
		}

		Array.from(uploadInput).forEach(async (file) => {
			try{
				await asyncXHR(file)
			}catch (err) {
				console.error(err)
			}
		})

	}
}


function addOnStartEventListeners() {
	// Responsive Upload Section
	let uploadLabel = document.querySelector("label[for='uploadinput']")
	let uploadInput = document.querySelector("#uploadinput")
	let uploadButton = document.querySelector("#upload")
	uploadLabel.addEventListener("click", (event) => {
		uploadInput.value = ""
		uploadLabel.innerText = "+ Click to Select Files"
	})
	uploadInput.addEventListener("input", (event) => {
		uploadLabel.innerText = `Selected ${uploadInput.files.length} files`
	})
	uploadButton.addEventListener("click", async (event) => { await uploadItems() })
}


window.onload = async (event) => {
	await getSharedItems("")
	addOnStartEventListeners()
}