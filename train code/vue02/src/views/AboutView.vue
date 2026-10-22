<template>
  <div id="app" class="container">
    <el-container style="justify-content: center;">
      <el-upload action="@assert/222_hidden.png" list-type="picture-card" :auto-upload="false">
        <i slot="default" class="el-icon-plus"></i>
        <div slot="file" slot-scope="{file}">
          <img class="el-upload-list__item-thumbnail" :src="file.url" alt="">
          <span class="el-upload-list__item-actions">
            <span class="el-upload-list__item-preview" @click="handlePictureCardPreview(file)">
              <i class="el-icon-zoom-in"></i>
            </span>
            <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleDownload(file)">
              <i class="el-icon-download"></i>
            </span>
            <span v-if="!disabled" class="el-upload-list__item-delete" @click="handleRemove(file)">
              <i class="el-icon-delete"></i>
            </span>
          </span>
        </div>
      </el-upload>
      <el-dialog :visible.sync="dialogVisible">
        <img width="100%" :src="dialogImageUrl" alt="">
      </el-dialog>
      
    </el-container>
  </div>
</template>


<script>
import axios from 'axios';
export default {
  data() {
    return {
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,
      watermarkText: '',
    };
  },
  methods: {
    handleRemove(file) {
      console.log(file);
    },
    handlePictureCardPreview(file) {
      console.log(file);

    },
    handleDownload(file) {
      console.log(file);
      // this.dialogImageUrl = file.url;
      // this.dialogVisible = true;
      fetch(file.url)
        .then(response => response.blob())
        .then(blob => {
          let formData = new FormData();
          formData.append('file', blob, 'image.png');
          axios.post('http://localhost:8081/decoder',formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
            .then(response => {
              this.watermarkText = response.data;
              alert("水印信息："+ this.watermarkText);

            })
            .catch(error => console.error(error));
        })
    }
  }
}
</script>







<style>
.container {
  justify-content: center;
  text-align: center;
  margin-top: 50px;
}

#watermark-output {
  margin-top: 20px;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>