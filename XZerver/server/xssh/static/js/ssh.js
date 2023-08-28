// Tech Defines
// ======================================================
let socket = io(`ws://${window.location.host}/ssh`, {
    reconnectionDelayMax: 3000
});

const terminal = document.querySelector('.terminal')
const term = new Terminal({
    rows: parseInt(terminal.getBoundingClientRect().height / 17),
    cols: parseInt(terminal.getBoundingClientRect().width / 10)
})
term.open(terminal)

let ssh_stat = false

const panel = document.querySelector(".flash-panel")
const html = document.createElement("section")
html.classList.add("flash")
const notify = new Notify(html, panel, 5000)

// Xterm Config
// ======================================================
term.onKey(async (e) => {
    if(e.key == "\u007f"){
        e.xkey = "\b \b"
    }else if(e.key == "\r"){
        e.xkey = "\n"
        await screen_updater()
    }else{
        e.xkey = e.key
    }
    if(ssh_stat){
        socket.emit("ssh_command", e.xkey)
        await screen_updater()
    }
})

// Socket Config
// ======================================================
socket.on("connect", () => {
    notify.addNotify("WebSocket Connected Successfully")
    console.log("WebSocket Connected Successfully")
})

socket.on("error", (err) => {
    notify.addNotify(`Error: ${err}`)
    console.log("Error: ", err)
})

socket.on("connection_stat", (stat) => {
    notify.addNotify(`SSH Connected: ${stat}`)
    console.log("SSH Connected: ", stat)
    ssh_stat = stat
})

socket.on("ssh_response", async (data) => {
    const text = new TextDecoder().decode(data)
    console.log(text)
    term.write(text)
    if(text != ""){
        await screen_updater()
    }
})

const screen_updater = async () => {
    socket.emit("screen_updater")
}

window.addEventListener("unload", (event) => {
    socket.close()
})

// UI Wiring
// ======================================================
const SSHConnectionStart = (event, form) => {
    event.preventDefault();
    term.reset()
    const formData = {
        hostname: form[0].value,
        port: form[1].value,
        username: form[2].value,
        password: form[3].value
    }
    if(formData.port == ""){
        formData.port = "22"
    }
    socket.emit("ssh_connect", formData)
}
