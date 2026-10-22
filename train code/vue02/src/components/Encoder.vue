<template>
    <div id="app" class="container">
        <el-container>
            <el-header>水印嵌入功能</el-header>
            <el-main>
                <el-form :model="numberValidateForm" ref="numberValidateForm" label-width="100px" class="demo-ruleForm">
                    <el-form-item label="水印信息" prop="age" :rules="[
                    { required: true, message: '水印信息不能为空' },
                    
                ]">
                        <el-input v-model="numberValidateForm.age" autocomplete="off"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="submitForm('numberValidateForm')">提交</el-button>
                        <el-button @click="resetForm('numberValidateForm')">重置</el-button>
                    </el-form-item>
                </el-form>
                
                <div id="watermark-output" v-if="watermarkedText">
                    <div>水印信息：{{ numberValidateForm.age }}</div>
                    <div class="block" v-for="fit in fits" :key="fit">
                        <span class="demonstration"></span>
                        

                        <el-image style="width: 200px; height:200px" :src="url" :fits="fit"></el-image>
                    </div>
                </div>
                

            </el-main>
        </el-container>
    </div>
</template>

<script>

import axios from 'axios';
export default {
    name: 'Encoder',
    data() {
        return {
            watermarkText: '',
            watermarkedText: false,
            avb : false,
            grayImageData: 'avc',
            numberValidateForm: {
                age: ''
            },
            fits: ['fill'],
            url: require('@/assets/111_hidden.png')
        }
    },
    methods: {
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    axios.post('http://localhost:8081/encoder', {
                        watermarking: this.numberValidateForm.age

                    })
                        .then(response => {
                            
                            this.watermarkedText =true;
                            this.avb =  this.watermarkedText;
                            console.log('this.watermarkedText:', this.watermarkedText);
                        })
                        .catch(error => {
                            console.error(error);
                        });


                } else {
                    console.log('error submit!!');
                    return false;
                }
            });

        },
        resetForm(formName) {
            this.$refs[formName].resetFields();   
            this.watermarkedText = false;
        },

    }
}
</script>

<style>
.container {
    text-align: center;
    margin-top: 50px;
}

#watermark-output {
    margin-top: 20px;
}
</style>