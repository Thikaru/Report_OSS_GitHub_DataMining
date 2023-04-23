#### ===============####
# git date csv化
#### ===============####
file_pointer = open("../csv/date_terraform.csv", "w")
commit_num_terraform = 0
with open('../git/date_commit_terraform.txt') as file:
    for line in file:
        date_array = line.split(' ')
        file_pointer.write(
            date_array[len(date_array)-2] + "," + date_array[len(date_array)-1])
        commit_num_terraform += int(date_array[len(date_array)-2])
file_pointer.close()
print("terafform" + str(commit_num_terraform))


file_pointer = open("../csv/date_vagrant.csv", "w")
commit_num_vagrant = 0
with open('../git/date_commit_vagrant.txt') as file:
    for line in file:
        date_array = line.split(' ')
        file_pointer.write(
            date_array[len(date_array)-2] + "," + date_array[len(date_array)-1])
        commit_num_vagrant += int(date_array[len(date_array)-2])
file_pointer.close()
print("vagrant : 合計"+str(commit_num_vagrant))

#### ===============####
# git top csv化
#### ===============####
file_pointer = open("../csv/top_terraform.csv", "w")
commit_num_terraform_top = 0
with open('../git/top_commiters_terraform.txt') as file:
    for line in file:
        date_array = line.split('	')
        file_pointer.write(
            date_array[len(date_array)-2] + "," + date_array[len(date_array)-1])
        commit_num_terraform_top += int(date_array[len(date_array)-2])
file_pointer.close()
print("top_terraform : 合計"+str(commit_num_terraform_top))

file_pointer = open("../csv/top_vagrant.csv", "w")
commit_num_vagrant_top = 0
with open('../git/top_commiters_vagrant.txt') as file:
    for line in file:
        date_array = line.split('	')
        file_pointer.write(
            date_array[len(date_array)-2] + "," + date_array[len(date_array)-1])
        commit_num_vagrant_top += int(date_array[len(date_array)-2])
file_pointer.close()
print("top_vagrant : 合計"+str(commit_num_vagrant_top))


file_pointer = open("../csv/top10_terraform.csv", "w")
commit_num_terraform_top = 0
with open('../git/Top10_terraform.txt') as file:
    for line in file:
        date_array = line.split('	')
        # print(date_array[len(date_array)-2])
        # print(date_array[len(date_array)-1])
        file_pointer.write(
            date_array[len(date_array)-2] + "," + date_array[len(date_array)-1])
        commit_num_terraform_top += int(date_array[len(date_array)-2])
file_pointer.close()
print("top_terraform : 合計"+str(commit_num_terraform_top))

file_pointer = open("../csv/top10_vagrant.csv", "w")
commit_num_vagrant_top = 0
with open('../git/Top10_vagrant.txt') as file:
    for line in file:
        date_array = line.split('	')
        # print(date_array[len(date_array)-2])
        # print(date_array[len(date_array)-1])
        file_pointer.write(
            date_array[len(date_array)-2] + "," + date_array[len(date_array)-1])
        commit_num_vagrant_top += int(date_array[len(date_array)-2])
file_pointer.close()
print("top_vagrant : 合計"+str(commit_num_vagrant_top))
