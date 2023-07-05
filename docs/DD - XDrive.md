## Story

**Goal?**
Achieve high speed transfers without a bloated software.

**What Purposes?**
I wanted to used a PC I had into a storage server, did experiment with SMB & SSH and both gave moderate performance with normal files, however with the files getting larger, integrity was diminishing. So I thought about using HTTP where it doesn't used heavy encryption like SSH and isn't relatively limited by how busy the network is in my 300Mbps router.

**Results?**
Tests resulted in 8 MB/s & 16 MB/s in terms of both uploads and downloads. Didn't test in production environment on my PC yet, but I have good hopes that this will go even further up as in tests the resources are divided on the same device between read & write. while on different machines, resource management will be more independent of each other.

## Usage

The app is built on top of a custom infrastructure I made where I don't have to run multiple servers when I add a new project. XDrive is an SPA that provides sharing features as Google Drive but with sharing options like Windows.

Going into the admin panel, a directory can be shared by adding it to XDrive model records. You specify:
* Display name `name field`.
* Absolute path `path field`. (This doesn't get shown in the frontend)
* Permissions `permissions field` (JSON filed that contains read/write permissions of account users.)
	* User `id` must be mentioned as a key for the user to get read permissions. `{"1": []}`
	* the word `write` must be appended as a list item to the value of the the user `id` to get write permissions. `{"1": ['write']}` Other values can be appended but will be neglected by the SPA. I just left this one as a feature for future feature expansions.

App works as follows:
1) On first load, App retrieves shared folders (`display name` & `id`) where the logged in user `id` is mentioned as a key in the permissions field.

2) User selects a folder using it's `id` and the app reads the directory and sends it back to the user along with directory statistics. Benefits of dealing with `id` is that you don't have to reveal the absolute path of your shared folder thus maintaining privacy.

3) If user has write permissions, upload box will be visible where you can select and upload files to the listed directory. Normal approach is that before sending files, SPA sends a GET request to the server verifying first whether the user has write permissions. If the returned response is `true` the algorithm continues with sending the files where the server side rechecks the write permissions for every POST request it gets, if not then it won't send.

4) Double click a file to download.

5) Select items using checkboxes and choose `Delete Selected` from the context menu to bulk delete them.

6) Create a New Folder using the `New Folder` option in the context menu.

7) **To Be Added:** Rename feature / Download folder as zip.