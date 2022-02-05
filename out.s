.data
       main_a: .word, 0
       main_test_0temp: .word, 0
       main_test_1temp: .word, 0
       main_test_2temp: .word, 0



.text
.globl main
main:
       PC0:
       li $v0, 5
       PC1:
       syscall
       PC2:
       sw $v0, main_test_0temp
       PC3:
       lw $t0, main_test_0temp
       PC4:
       sw $t0, main_a
       PC5:
       lw $t0, main_a
       PC6:
       lw $t1, main_a
       PC7:
       mul $t2, $t0, $t1
       PC8:
       sw $t2, main_test_1temp
       PC9:
       lw $t0, main_test_1temp
       PC10:
       lw $t1, main_a
       PC11:
       mul $t2, $t0, $t1
       PC12:
       sw $t2, main_test_2temp
       PC13:
       li $v0, 1
       PC14:
       lw $a0, main_test_2temp
       PC15:
       syscall
       PC16:



exit:
       li $v0, 10
       syscall