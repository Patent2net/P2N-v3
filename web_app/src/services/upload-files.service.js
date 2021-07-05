
class UploadFilesService {
  upload(file) {
    let formData = new FormData();

    formData.append("file", file);

    return fetch("http://localhost:5000/api/v1/csv/upload", {
        method: 'POST',
        body: formData,
    }).then((response) => response.json());
  }

  getFiles() {
    return fetch("http://localhost:5000/api/v1/csv/list", { method: 'GET' }).then((response) => response.json());
  }
}

export default new UploadFilesService();