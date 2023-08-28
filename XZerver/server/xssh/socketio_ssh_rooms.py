from paramiko import SSHClient, AutoAddPolicy

class SocketIORooms():
	def __init__(self):
		super(SocketIORooms, self).__init__()
		self.__rooms = {}

	def create_room(self, room_id) -> None:
		ssh_client = SSHClient()
		ssh_client.load_host_keys("./instance/ssh_known_hosts")
		ssh_client.set_missing_host_key_policy(AutoAddPolicy())
		self.__rooms[room_id] = {
			"ssh_client": ssh_client,
			"ssh_shell": None
		}

	def close_room(self, room_id) -> None:
		self.__rooms.pop(room_id, None)

	def get_client(self, room_id):
		room = self.__rooms.get(room_id, None)
		if room:
			return room["ssh_client"]
		return None

	def get_shell(self, room_id):
		room = self.__rooms.get(room_id, None)
		if room and room.get("ssh_shell", None):
			return room["ssh_shell"]
		return None

	def invoke_shell(self, room_id, shell) -> None:
		self.__rooms[room_id]["ssh_shell"] = shell

socketio_rooms = SocketIORooms()