#include<stdio.h>
#include<string.h>
#include<stdlib.h>

#define MAX_LINE_LEN 1024
#define MAX_PROFILES 10000  /*保存できる名簿の最大値*/


int stop_addData_Flag = 0;  /*データが10000件保存して追加で保存されようとしているときに警告文を出力するときの条件文に使用*/
int is_overwriteMode = 0;  /*上書きモードの変更に使用*/
int profile_data_nitems = 0;  /*グローバル変数 名簿の一つ一つの配列の場所を指定*/
int profile_data_changeIndex = 0;  /*上書きモードでデータの保存に使う変数*/

  /*誕生日の年月日の構造体*/
struct date{
	int year;
	int month;
	int day;
};

	/*文字列を5つにしたものを保存する構造体*/
struct profile{
	int id;
	char name[70];
	struct date birthday;
	char address[70];
	char *other;
};

	/*構造体profile型のprofile_data_storeという名簿を保存しておく，配列を条件通り最大10000件保存できるように宣言*/
struct profile profile_data_store[MAX_PROFILES];

/*プロトタイプ宣言*/
int subst(char *str, char c1, char c2);
int split(char *str, char *ret[],char sep, int max);
int get_line(FILE *fp, char *line);
void cmd_quit();
void cmd_check();
void cmd_print(int figure);
void cmd_read(char *word);
void cmd_write(char *filename);
void cmd_find(char *place);
int sort_compare(struct profile *p1,struct profile *p2, int order);
void swap_struct(struct profile *p1, struct profile *p2);
void figure_quick_sort(int low,int high,int order);
void cmd_sort(int order);
void cmd_overwrite();
void exec_command(char cmd, char *param);
struct date *new_date(struct date *d,char *str);
struct profile *new_profile(struct profile *p,char *csv);
void parse_line(char *line);

/*----------------------------------------------------------------------------*/
int main(){
	/*一行入力で1024文字と制限するので1024文字
		と改行文字の一文字を加えた1025文字を保存できる配列を宣言*/
	char line[MAX_LINE_LEN + 1];
	
	while (get_line(stdin, line)) {
		parse_line(line);
	}
	return 0;
}

/*----------------------------------------------------------------------------*/
	/*
	subst関数
	*str：文字列
	c1：変更したい文字
	c2：変更する文字
	*/
int subst(char *str, char c1, char c2){
	int n = 0;
	
	while(*str != '\0'){ 
		if(*str == c1){
			*str = c2;
			n += 1;
		}
		str += 1;
	}
	return n;
}

/*----------------------------------------------------------------------------*/
	/*
	<引数の説明>
	*str：分割したい文字列
	*ret：分割した文字列の先頭アドレスを保存する配列ポインタ
	sep：分割したい区切り文字
	max：分割最大数
	*/
int split(char *str, char *ret[],char sep, int max){
	int cut = 0;
	ret[cut] = str;
	cut+=1;
	
		while(*str != '\0' && cut < max)  {
			if(*str == sep){
				*str = '\0';
				ret[cut] = str + 1; 
				cut += 1;
			} 
			str++;
		}
	return cut;
}

/*----------------------------------------------------------------------------*/
int get_line(FILE *fp, char *line){
		/*fgetsで一行の入力1024行プラス改行文字の1025文字と制限して行う．実行できたら，
			elseの方に移りsubst関数でエンターキーでの改行文字を終端文字に変換する．*/
	if(fgets(line, MAX_LINE_LEN + 1, fp) == NULL){
		return 0;
	}else{
		subst(line, '\n', '\0');
		return 1;
	}
}

/*----------------------------------------------------------------------------*/
void cmd_quit(){
	exit(0);
}

/*----------------------------------------------------------------------------*/
void cmd_check(){
	printf("%d profile(s)\n",profile_data_nitems);
}
/*----------------------------------------------------------------------------*/
	/*
	printコマンド関数
	<説明>
	figureの数字分データを出力(保存データ数より大きい場合もすべてを出力)
	正の数：先頭から
	負の数：後ろから
	0：すべてのデータを出力
	*/
void cmd_print(int figure){
	int first_print,last_print;
	
	if(figure == 0){
		first_print = 0;
		last_print = profile_data_nitems;
	}else if(figure > 0){
		if(figure <= profile_data_nitems){
			first_print = 0;
			last_print = figure;
		}else{
			first_print = 0;
			last_print = profile_data_nitems;
		}
	}else if(figure <0){
		if((-1)*figure <= profile_data_nitems){
			first_print = profile_data_nitems + figure;
			last_print = profile_data_nitems;
		}else{
			first_print = 0;
			last_print = profile_data_nitems;
		}
	}while(first_print != last_print ){
		/*何番目のデータか知りたいなら追加printf("data_number %d\n",first_print+1);*/
		printf("data_number %d\n",first_print+1);
		printf("Id    : %d\n",profile_data_store[first_print].id);
		printf("Name  : %s\n",profile_data_store[first_print].name);
		printf("Birth : %04d-%02d-%02d\n",profile_data_store[first_print].birthday.year,
			profile_data_store[first_print].birthday.month,profile_data_store[first_print].birthday.day);
		printf("Addr. : %s\n",profile_data_store[first_print].address);
		printf("Comm. : %s\n",profile_data_store[first_print].other);
		first_print += 1;
	}
	printf("%%Pコマンドを実行しました．\n\n");
}

/*----------------------------------------------------------------------------*/
void cmd_read(char *filename){
	char length[MAX_LINE_LEN + 1];
	FILE *fp;
	fp = fopen(filename, "r");
	if(fp == NULL){
		fprintf(stderr,"%%R: file open error .\n\n");
	}else{ 
		while(get_line(fp, length) != 0){
			parse_line(length);
		}
		fclose(fp);
		printf("%%Rコマンドで%sファイルを読み込みました．\n\n",filename);
	}
}

/*----------------------------------------------------------------------------*/
void cmd_write(char *filename){ 
	FILE *fp;
	int i; 
	
	fp = fopen(filename, "w");
	if(fp == NULL){
		fprintf(stderr,"%%W: file open error .\n\n");
	}else{
		for(i=0; i<profile_data_nitems; i++){
			fprintf(fp,"%d,",profile_data_store[i].id);
			fprintf(fp,"%s,",profile_data_store[i].name);
			fprintf(fp,"%04d-",profile_data_store[i].birthday.year);
			fprintf(fp,"%02d-",profile_data_store[i].birthday.month);
			fprintf(fp,"%02d,",profile_data_store[i].birthday.day);
			fprintf(fp,"%s,",profile_data_store[i].address);
			fprintf(fp,"%s\n",profile_data_store[i].other);
		}
		fclose(fp);
		printf("%%Wコマンドで%sファイルに保存データを書き込みました．\n\n",filename);
	}
}

/*----------------------------------------------------------------------------*/
void cmd_find(char *word){
	/*
	<変数名説明>
	f：保存データすべてを探すために使う変数
	match_data_num：検索ワードと一致するデータあると1を加える．データを出力する判定に使う(1以上かどうか)
	missMatch_data：合致していないデータ数を数える
	id_string[]：IDを文字列に変更する
	birth1：year-month-day(2021-01-01) %04d-%02d-$02d
	birth2：year-month-day(2021-1-1)   %d-%d-%d
	*/
	int f,match_data_num,missMatch_data=0;
	char id_string[10];
	char birth1[11],birth2[11];
	
		/*改行文字が終端文字に変更していないと文字列も比較の時エラーが出るので
		改行に使われる，\nとアスキー文字コードで^Mを表す13をsubst関数を使って終端文字に変更している．*/
	subst(word, '\n', '\0');
	subst(word, 13, '\0');
	
	printf("%%Fコマンドで%sを検索しました．\n",word);
	
	for(f=0;f<profile_data_nitems;f++){
		match_data_num = 0;
		sprintf(id_string,"%d",profile_data_store[f].id);
		if(strcmp(id_string,word)==0){
			match_data_num++;
		}
		
		if(strcmp(profile_data_store[f].name,word)==0||
			strcmp(profile_data_store[f].address,word)==0||
			strcmp(profile_data_store[f].other,word)==0){
			match_data_num++;
		}
		
		sprintf(birth1,"%04d-%02d-%02d",profile_data_store[f].birthday.year,
			profile_data_store[f].birthday.month,profile_data_store[f].birthday.day);
		sprintf(birth2,"%d-%d-%d",profile_data_store[f].birthday.year,
			profile_data_store[f].birthday.month,profile_data_store[f].birthday.day);
		if(strcmp(birth1,word)==0||strcmp(birth2,word)==0){
			match_data_num++;
		}
		
		if(match_data_num>=1){
				/*何番目のデータか知りたいなら追加printf("data_number %d\n",i+1);*/
			printf("Id    : %d\n",profile_data_store[f].id);
			printf("Name  : %s\n",profile_data_store[f].name);
			printf("Birth : %04d-%02d-%02d\n",profile_data_store[f].birthday.year,
			profile_data_store[f].birthday.month,profile_data_store[f].birthday.day);
			printf("Addr. : %s\n",profile_data_store[f].address);
			printf("Comm. : %s\n\n",profile_data_store[f].other);
		}else{/*もしあてはあるものなかったらmissMatch_dataに1を追加する*/
			missMatch_data++;
		}
	}
	if(missMatch_data == profile_data_nitems){
		fprintf(stderr,"見つかりませんでした．\n");
	}
}

/*----------------------------------------------------------------------------*/
int sort_compare(struct profile *p1,struct profile *p2, int order){	
	switch(order){
		case 1: {
			return (p1->id - p2->id);
			break;
		}
		case 2: {
			return strcmp(p1->name,p2->name);
			break;
		}
		case 3:{
			int f=0;
			if((p1->birthday.year)!=(p2->birthday.year)){
				f = p1->birthday.year - p2->birthday.year;
				return f;
			}else if((p1->birthday.month)!=(p2->birthday.month)){
				f = p1->birthday.month - p2->birthday.month;
				return f;
			}else if((p1->birthday.day)!=(p2->birthday.day)){
				f = p1->birthday.day - p2->birthday.day;
				return f;
			}
			break;
		}
		case 4: {
			return strcmp(p1->address,p2->address);
			break;
		}
		case 5:{
			return strcmp(p1->other,p2->other);
			break;
		}
	}
	return 0;
}

/*----------------------------------------------------------------------------*/
void swap_struct(struct profile *p1, struct profile *p2){
	struct profile tmp;
	tmp = *p1;
	*p1 = *p2;
	*p2 = tmp;
}
/*----------------------------------------------------------------------------*/
void quick_sort(int left, int right,int order){
	int mid = (left + right) / 2;
	int l = left, r = right;
	
	if (left < right){
		while (l <= r) {
			while (sort_compare(&profile_data_store[mid], &profile_data_store[l],order) >  0) {
				l++;
			}
			while (sort_compare(&profile_data_store[mid], &profile_data_store[r],order) <  0){
				r--;
			}
			if (l <= r){
				if(mid == l){
					mid = r;
				}else if(mid == r){
					mid = l;
				}
				swap_struct(&profile_data_store[l++], &profile_data_store[r--]);
			}
		}
	quick_sort(left, r, order);
	quick_sort(l, right, order);
	}
}
	
/*----------------------------------------------------------------------------*/
	/*
	保存されたデータを引数の数番目の要素ごとにソートする関数
	<引数>
	1：IDごとに昇順
	2：NAMEの辞書順
	3：BIRTHDAYの昇順
	4：ADDRESSの辞書順
	5：OTHERの辞書順
	*/
void cmd_sort(int order){
	if(1<=order && order<=5){
		quick_sort(0,profile_data_nitems-1,order);
		printf("要素 %d でソートが完了しました\n",order);
		if(profile_data_nitems == MAX_PROFILES && is_overwriteMode == 1){	/*保存数が10000件の時にソートを行ったら上書きの場所を先頭に戻す*/
			profile_data_changeIndex = 0;
		}
	}else{
		fprintf(stderr,"あなたが入力した数=%dではソートできません．1から5の数を入力してください．\n",order);
	}
}

/*----------------------------------------------------------------------------*/
/*上書きモードON(1),OFF(0)を変更する関数*/
void cmd_overwrite(){
	if(is_overwriteMode == 0){
		printf("%%Oを実行しました．\n%d件のデータを保存した場合，それ以降の新規データは先頭に保存されます．\n",MAX_PROFILES);
		is_overwriteMode = 1;
		if(profile_data_nitems < MAX_PROFILES){
			profile_data_changeIndex = profile_data_nitems;
		}else if(profile_data_nitems == MAX_PROFILES){
			profile_data_changeIndex = 0;
		}
	}else if(is_overwriteMode == 1){
		printf("%%Oを実行しました．\nデータの上書きをせずに%d件を超えるとデータを保存しません．\n",MAX_PROFILES);
		is_overwriteMode = 0;
		stop_addData_Flag = 0; /*MAX_PROFILES件を超えたときに出るメッセージをもう一度出るようにする*/
	}
}
/*----------------------------------------------------------------------------*/
	/*入力されたコマンドを識別する関数
	<コマンドごとの説明>
	%Q：<%Q>         プログラムを終了
	%C：<%C>         保存データ数を出力
	%P：<%P number>  引数の数分データを出力(正の数：先頭から　負の数：後ろから 0ならすべて)
	%R：<%R filename>ファイルを読み込む
	%W：<%W filename>現在保存データをファイルに書き出す
	%S：<%S number>  引数の数の要素ごとにソートする
	%O：<%O>         上書き許可，禁止を切り替える(default：禁止)
	*/
void exec_command(char cmd, char *param){
	switch (cmd) {
	case 'Q': cmd_quit(); break;
	case 'C': cmd_check(); break;
	case 'P':{
			if(('0'<=param[0]&&param[0]<='9')||(param[0]=='-' && '0'<=param[1]&&param[1]<='9') ){
				cmd_print(atoi(param));
			}else{
				printf("数字を入力してください．\n");
			}
			break;
		}
	case 'R': cmd_read(param);break;
	case 'W': cmd_write(param); break;
	case 'F': cmd_find(param); break;
	case 'S': cmd_sort(atoi(param)); break;
	case 'O': cmd_overwrite(); break;
	default:
		fprintf(stderr,"Invalid command %c: ignored.\n\n",cmd);
		break;
	}
}
/*----------------------------------------------------------------------------*/
	/*誕生日を年月日に分けるための関数
	「year-month-day」　データを受け付ける
	*/
struct date *new_date(struct date *d,char *str){
	char *ptr[3];
	
	if(split(str, ptr, '-', 3) != 3){
		return NULL;
	}
	d->year = atoi(ptr[0]);
	d->month = atoi(ptr[1]);
	d->day = atoi(ptr[2]);
	
	return d;
}
/*----------------------------------------------------------------------------*/
	/*
	下記の区切りデータを構造体に分割して保存する関数(返値：構造体のアドレス)
	「ID,name,birthday,address,other」　データを使用
	*/
struct profile *new_profile(struct profile *p,char *csv){
	char *ptr[5];
	
	if(split(csv, ptr, ',', 5) != 5){
		if(is_overwriteMode==0){	/*要素が5つないときに保存場所を使用するのを防ぐ*/
			profile_data_nitems = profile_data_nitems - 1;
		}else if(is_overwriteMode==1){
			profile_data_changeIndex = profile_data_changeIndex - 1;
		}
		
		fprintf(stderr, "your data is not five factors．\n");
		return NULL;
	}
	p->id = atoi(ptr[0]);
	strncpy(p->name, ptr[1], 70);
	p->name[69] = '\0';
	
	if(new_date(&p->birthday, ptr[2]) == NULL){
		return NULL;
	}
	
	strncpy(p->address, ptr[3], 70);
	p->address[69] = '\0';
	
	p->other = (char *)malloc(sizeof(char) * (strlen(ptr[4])+1));
	strcpy(p->other, ptr[4]);
	
	return p;
}

/*----------------------------------------------------------------------------*/
	/*
	コマンドなのか文字列なのかを識別し，処理を他の関数に移行する処理を行う関数
	<上書きモード>
	MAX_PROFILESを超えるまでは，通常モードと同じようにデータを追加
	超えると，先頭から追加データを保存するようになる
	*/
void parse_line(char *line){
	
	if (line[0] == '%'&& line[2] != ' ' && line[1] != 'Q' && line[1] != 'C'&&line[1]!='O') {
		if(line[1]=='P'|| line[1]=='F'|| line[1]=='R' ||line[1]=='W'|| line[1]=='S'){	/*コマンドで追加データを使用するものの空白がないことを通知*/
			fprintf(stderr,"Your input command%%%c Not blank．line[2]=%c\n",line[1],line[2]);
		}else{
			exec_command(line[1],&line[3]);
		}
	}else if(line[0] == '%'){
		exec_command(line[1],&line[3]);
	}else{
		if(is_overwriteMode == 0){
			if(profile_data_nitems != MAX_PROFILES){	/*データの保存数が10000件を超えたときに保存を中止するようにするための条件文*/
				new_profile(&profile_data_store[profile_data_nitems++], line);
			}else if(stop_addData_Flag==0){
				printf("%d件のデータが保存されています．新しく保存する場合は上書きモードにコマンド%%Oで変更してください．\n",MAX_PROFILES);
				stop_addData_Flag = 1;
			}
		}else if(is_overwriteMode == 1){
			if(profile_data_changeIndex < MAX_PROFILES){	/*上書き場所によって書き込む場所を変更するかを判断*/
				if(profile_data_nitems != MAX_PROFILES){	/*データを10000件未満の場合は追加保存する前に10000件までデータを保存させる*/
					new_profile(&profile_data_store[profile_data_changeIndex++], line);
					profile_data_nitems++;	/*上書きモード終了後では，profile_data_nitems使用するので数字を1追加しておく*/
				}else if(profile_data_nitems==MAX_PROFILES){
					new_profile(&profile_data_store[profile_data_changeIndex++], line);
				}
			}else if(profile_data_changeIndex==MAX_PROFILES){	/*上書き場所の更新*/
				profile_data_changeIndex = 0;
				new_profile(&profile_data_store[profile_data_changeIndex++], line);
			}
		}
	}
}