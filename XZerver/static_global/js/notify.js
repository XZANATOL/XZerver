/*
Used in:
	- xssh
*/

class Notify{
	constructor(html, panel, timeout = 1000){
		this.html = html
		this.panel = panel
		this.timeout = timeout
		this.count = 0
	}

	addNotify(text){
		let element = this.html.cloneNode(true)
		element.innerText = text
		element.id = `flash-${this.count}`

		setTimeout((count) => {
			let del = document.querySelector(`#flash-${count}`)
			del.remove()
		}, this.timeout, this.count)
		
		this.count += 1
		this.panel.appendChild(element)
	}
}