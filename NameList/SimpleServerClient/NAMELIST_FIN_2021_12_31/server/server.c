/*library------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

/*define-----------------------------------------------------*/
#define MAX_LISTEN 5
#define MAX_LINE_LEN 2048
#define MAX_PROFILES 10000  /*保存できる名簿の最大値*/
#define PORT 54321

/*struct-----------------------------------------------------*/
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

/*global-----------------------------------------------------*/
		/*名簿管理用グローバル変数*/
int StopAddDataFlag = 0;          /*データが10000件保存して追加で保存されようとしているときに警告文を出力するときの条件文に使用*/
int IsOverwriteMode = 0;          /*上書きモードの変更に使用*/
int profile_data_nitems = 0;      /*グローバル変数 名簿の一つ一つの配列の場所を指定*/
int profile_data_changeIndex = 0; /*上書きモードでデータの保存に使う変数*/
int IsStartCmdR = 0;              /*cmdR使用時にデータ保存の確認出力を一度にするための判断用変数*/
int AuthorityLevel = 0;           /* 権限レベル：0(一般)，1(管理者)*/
int IsServerPreserveData = 0;     /*0：クライアント側，1：サーバ側 データを保存*/
int IsCmdRServerFile = 0;         /*サーバ側のファイルを読むかどうか 0:クライアント 1:サーバ*/
int IsConnectionFlag = 0;         /*接続済みのクライアントがいるかどうか*/

char FinishMessage[] = "FINISH";
char ErrorArg[] = "Error:argument\n";
char ErrorSocket[] = "Error:socket\n";
char ErrorAccept[] = "Error:accept\n";
char ErrorListen[] = "Error:listen\n";
char ErrorSend[] = "Error:send\n";
char ErrorRecv[] = "Error:recv\n";
char ErrorBind[] = "Error:bind\n";
char ConectionWaitMessage[] ="Waiting for connection\n";
char SuccessConnectionMessage[] = "Connected from ";
/*構造体profile型のprofile_data_storeという名簿を保存しておく，配列を条件通り最大10000件保存できるように宣言*/
struct profile profile_data_store[MAX_PROFILES];

/*prototype declare------------------------------------------*/
int Char_Num_Count(char string[]);
void Send_Server2client(int socket, char *str);
void Recv_Client_Data(int socket, char *str);
void Judge_AuthorityLevel(int socket);

int subst(char *str, char c1, char c2);
int split(char *str, char *ret[],char sep, int max);
int get_line(FILE *fp, char *line);
void cmd_quit(int socket);
void cmd_check(int socket);
void cmd_print(int socket, int figure);
void cmd_read(int socket, char *word);
void cmd_write(int socket, char *filename);
void cmd_find(int socket, char *place);
int sort_compare(struct profile *p1,struct profile *p2, int order);
void swap_struct(struct profile *p1, struct profile *p2);
void figure_quick_sort(int low,int high,int order);
void cmd_sort(int socket, int order);
void cmd_overwrite(int socket);
void cmd_authority(int socket);
void exec_command(int socket, char cmd, char *param);
struct date *new_date(struct date *d,char *str);
struct profile *new_profile(int socket, struct profile *p,char *csv);
void parse_line(int socket, char *line);

/*server-----------------------------------------------------------------*/

int main(int argc, char const *argv[]){
	int server_socket;
	int client_socket;
	socklen_t dstAddrSize;
	struct sockaddr_in SourceAddr,DestinationAddr;
	int strLen;
	char *receivebuffer;
	
	
	//①socket
	server_socket = socket(AF_INET, SOCK_STREAM, 0);
	if(server_socket == -1){
		write(2,ErrorSocket,Char_Num_Count(ErrorSocket));
	}
	
	//②bind
	memset((char*)&SourceAddr, 0, sizeof(SourceAddr));
	SourceAddr.sin_family = AF_INET;
	SourceAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	SourceAddr.sin_port=htons(PORT);
	if(bind(server_socket, (struct sockaddr *)&SourceAddr, sizeof(SourceAddr)) == -1){
		write(2, ErrorBind, Char_Num_Count(ErrorBind));
	}
	
	//③listen
	if(listen(server_socket, MAX_LISTEN) == -1){
		write(2, ErrorListen, Char_Num_Count(ErrorListen));
	}
	
	//④accept
	while(1){
		printf("%%%%----------------------------------%%%%\n");
		write(1,ConectionWaitMessage, Char_Num_Count(ConectionWaitMessage) );
		dstAddrSize = sizeof(DestinationAddr);
		if( (client_socket = accept(server_socket, (struct sockaddr *)&DestinationAddr, &dstAddrSize) ) == -1){
			write(2, ErrorAccept, Char_Num_Count(ErrorAccept));
		}
		write(1,SuccessConnectionMessage,Char_Num_Count(SuccessConnectionMessage) );
		write(1,inet_ntoa(DestinationAddr.sin_addr),Char_Num_Count(inet_ntoa(DestinationAddr.sin_addr)) );
		write(1,"\n",1);
		IsConnectionFlag = 1;
		
		//権限判断
		Judge_AuthorityLevel(client_socket);
		
		//クライアントとの通信部分
		while(1){
			receivebuffer = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
			memset(receivebuffer, 0, MAX_LINE_LEN);
			if( (strLen = recv(client_socket, receivebuffer, MAX_LINE_LEN, 0) ) == -1 ){
				write(2, ErrorRecv, Char_Num_Count(ErrorRecv));
			}
			subst(receivebuffer , '\n', '\0');
			/*名簿管理プログラムの判定開始*/
			parse_line(client_socket,receivebuffer);
			
			free(receivebuffer);
			if(IsConnectionFlag == 0){
				break;
			}
		}
	}
	//⑦ソケットを削除
	close(server_socket);
}

/*関数--------------------------------------------------------------------*/
void Send_Server2client(int socket, char *str){
	int strSize;
	char *tmpStr;
	
	tmpStr = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
	memset(tmpStr, 0, MAX_LINE_LEN);
	sprintf(tmpStr, "%s",str);
	if( (strSize = send(socket, str ,MAX_LINE_LEN, 0) ) == -1){
		write(2,ErrorSend,Char_Num_Count(ErrorSend) );
	}
	free(tmpStr);
}

/*----------------------------------------------------------------------------*/
void Recv_Client_Data(int socket, char *str){
	int check;
	
	if( (check = recv(socket, str, MAX_LINE_LEN, 0)) == -1){
		write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
	}
}

/*----------------------------------------------------------------------------*/
int Char_Num_Count(char string[]){
	int i=0;
	for(i=0; string[i] != '\0'; i++){;}
	
	return i;
}

/*----------------------------------------------------------------------------*/
void Judge_AuthorityLevel(int socket){
	char sendbuffer[MAX_LINE_LEN];
	char receivebuffer[MAX_LINE_LEN];
	int check;
	
	memset(receivebuffer, 0, MAX_LINE_LEN);
	if( (check = recv(socket, receivebuffer, MAX_LINE_LEN, 0) ) == -1 ){
		write(2, ErrorRecv, Char_Num_Count(ErrorRecv));
	}
	
	memset(sendbuffer, 0, MAX_LINE_LEN);
	if(strcmp(receivebuffer, "ADMIN") == 0){
		printf("CLIENT IS ADMINISTRATOR!\n\n");
		sprintf(sendbuffer,"YOUR ADMINISTRATOR");
		Send_Server2client(socket, sendbuffer);
		AuthorityLevel = 1;
	}else{
		printf("CLIENT IS NORMAL USER!\n\n");
		sprintf(sendbuffer,"YOUR NORMAL USER");
		Send_Server2client(socket, sendbuffer);
		AuthorityLevel = 0;
	}
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
		/*fgetsで一行の入力MAX_LINELEN行プラス改行文字のMAX_LINE_LEN+1文字と制限して行う．実行できたら，
			elseの方に移りsubst関数でエンターキーでの改行文字を終端文字に変換する．*/
	if(fgets(line, MAX_LINE_LEN + 1, fp) == NULL){
		return 0;
	}else{
		subst(line, '\n', '\0');
		return 1;
	}
}

/*----------------------------------------------------------------------------*/
void cmd_quit(int socket){
	char str[MAX_LINE_LEN];
	
	memset(str, 0, MAX_LINE_LEN);
	sprintf(str, "Good Bye!!\n");
	Send_Server2client(socket, str);
	close(socket);
	//次の通信相手のために初期化
	IsConnectionFlag = 0;
	AuthorityLevel = 0;
	IsServerPreserveData = 0;
	IsCmdRServerFile = 0;
}

/*----------------------------------------------------------------------------*/
void cmd_check(int socket){
	char str[MAX_LINE_LEN];
	memset(str, 0, MAX_LINE_LEN);
	sprintf(str, "%d  profile(s)\n",profile_data_nitems);
	Send_Server2client(socket, str);
	printf("%%Cが実行されました．\n");
	fflush(stdout);
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
void cmd_print(int socket, int figure){
	int first_print,last_print;
	char *strMemberData;
	
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
	}
	
	while( first_print != last_print+1 ){
		if(first_print != last_print){
		/*何番目のデータか知りたいなら追加printf("data_number %d\n",first_print+1);*/
			strMemberData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
			memset(strMemberData, 0, MAX_LINE_LEN);
			sprintf(strMemberData,"data_number %d\n",first_print+1);
			sprintf(strMemberData,"%sId    : %d\n",strMemberData,profile_data_store[first_print].id);
			sprintf(strMemberData,"%sName  : %s\n",strMemberData,profile_data_store[first_print].name);
			sprintf(strMemberData,"%sBirth : %04d-%02d-%02d\n",strMemberData,profile_data_store[first_print].birthday.year,
				profile_data_store[first_print].birthday.month,profile_data_store[first_print].birthday.day);
			sprintf(strMemberData,"%sAddr. : %s\n",strMemberData,profile_data_store[first_print].address);
			sprintf(strMemberData,"%sComm. : %s\n\n",strMemberData,profile_data_store[first_print].other);
		}else{
			strMemberData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
			memset(strMemberData, 0, MAX_LINE_LEN);
			sprintf(strMemberData,"%s",FinishMessage);
		}
		
		Send_Server2client(socket, strMemberData);
		free(strMemberData);
		
		first_print += 1;
	}
	printf("%%Pを実行しました．\n");
}

/*----------------------------------------------------------------------------*/
void cmd_read(int socket, char *filename){
	char InputLineLength[MAX_LINE_LEN];
	char str[MAX_LINE_LEN];
	FILE *fp;
	int loadCount=0;
	
	IsStartCmdR = 1;
	if(IsCmdRServerFile == 1){
		fp = fopen(filename, "r");
		if(fp == NULL){
			fprintf(stderr,"%%R: file open error .\n\n");
			memset(str, 0, MAX_LINE_LEN);
			sprintf(str,"%%R: file open error .\n\n");
			Send_Server2client(socket, str);
		}else{ 
			while(get_line(fp, InputLineLength) != 0){
				parse_line(socket, InputLineLength);
			}
			fclose(fp);
			if(profile_data_nitems == MAX_PROFILES){
				printf("%d件を超えました\n",MAX_PROFILES);
				memset(str, 0, MAX_LINE_LEN);
				sprintf(str, "%d件を超えました\n",MAX_PROFILES);
				Send_Server2client(socket, str);
			}else{
				printf("%%Rコマンドで%sファイルを読み込みました．\n",filename);
				memset(str, 0, MAX_LINE_LEN);
				sprintf(str, "Read %s\n", filename);
				Send_Server2client(socket, str);
			}
		}
	}else if(IsCmdRServerFile == 0){
		while(1){
			memset(str, 0, MAX_LINE_LEN);
			Recv_Client_Data( socket, str);
			
			if(strcmp(str, FinishMessage) == 0){
				if(loadCount == 0){
					printf("%%Rコマンドで%sは中身が空か，ファイルが開けてません\n",filename);
					memset(str, 0, MAX_LINE_LEN);
					sprintf(str, "%%Rコマンドで%sは中身が空か，ファイルが開けてません\n",filename);
					Send_Server2client(socket, str);
				}
				break;
			}
			parse_line(socket, str);
			loadCount++;
		}
		printf("%%Rは実行されました．\n");
	}
	IsStartCmdR = 0;
}

/*----------------------------------------------------------------------------*/
void cmd_write(int socket, char *filename){ 
	FILE *fp;
	int i; 
	char sendmessage[MAX_LINE_LEN];
	
	if(IsServerPreserveData == 1){

		fp = fopen(filename, "w");
		if(fp == NULL){
			fprintf(stderr,"%%W: file open error .\n\n");
			memset(sendmessage, 0, MAX_LINE_LEN);
			sprintf(sendmessage, "Read %s\n", filename);
			Send_Server2client(socket, "%%W: file open error .\n\n");
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
			memset( sendmessage, 0, MAX_LINE_LEN);
			sprintf(sendmessage,"%%Wコマンドで%sファイルに保存データを書き込みました．\n\n",filename);
			Send_Server2client(socket, sendmessage);
		}
		printf("%%Wでserver側に%sに書き込みました．\n",filename);
	}else if(IsServerPreserveData == 0){
		for(i=0; i<profile_data_nitems+1; i++){
			memset( sendmessage, 0, MAX_LINE_LEN);
			if(i<profile_data_nitems){
				sprintf(sendmessage,"%s%d,",sendmessage,profile_data_store[i].id);
				sprintf(sendmessage,"%s%s,",sendmessage,profile_data_store[i].name);
				sprintf(sendmessage,"%s%04d-%02d-%02d,",sendmessage,profile_data_store[i].birthday.year,
					profile_data_store[i].birthday.month,profile_data_store[i].birthday.day);
				sprintf(sendmessage,"%s%s,",sendmessage,profile_data_store[i].address);
				sprintf(sendmessage,"%s%s",sendmessage,profile_data_store[i].other);
			}else{
				sprintf(sendmessage,"%s",FinishMessage);
			}
			Send_Server2client(socket, sendmessage);
		}
	printf("%%Wでclient側に%sに書き込みました．\n",filename);
	}
}

/*----------------------------------------------------------------------------*/
void cmd_find(int socket, char *word){
	/*
	<変数名説明>
	f：保存データすべてを探すために使う変数
	matchDataNum：検索ワードと一致するデータあると1を加える．データを出力する判定に使う(1以上かどうか)
	missMatchData：合致していないデータ数を数える
	id_string[]：IDを文字列に変更する
	birth1：year-month-day(2021-01-01) %04d-%02d-$02d
	birth2：year-month-day(2021-1-1)   %d-%d-%d
	*/
	int f,matchDataNum,missMatchData=0;
	char id_string[10];
	char birth1[11],birth2[11];
	char sendmessage[MAX_LINE_LEN];
	
		/*改行文字が終端文字に変更していないと文字列も比較の時エラーが出るので
		改行に使われる，\nとアスキー文字コードで^Mを表す13をsubst関数を使って終端文字に変更している．*/
	subst(word, '\n', '\0');
	subst(word, 13, '\0');
	
	for(f=0;f<profile_data_nitems;f++){
		matchDataNum = 0;
		sprintf(id_string,"%d",profile_data_store[f].id);
		if(strcmp(id_string,word)==0){
			matchDataNum++;
		}
		
		if(strcmp(profile_data_store[f].name,word)==0||
			strcmp(profile_data_store[f].address,word)==0||
			strcmp(profile_data_store[f].other,word)==0){
			matchDataNum++;
		}
		
		sprintf(birth1,"%04d-%02d-%02d",profile_data_store[f].birthday.year,
			profile_data_store[f].birthday.month,profile_data_store[f].birthday.day);
		sprintf(birth2,"%d-%d-%d",profile_data_store[f].birthday.year,
			profile_data_store[f].birthday.month,profile_data_store[f].birthday.day);
		if(strcmp(birth1,word)==0||strcmp(birth2,word)==0){
			matchDataNum++;
		}
		
		if(matchDataNum>=1){
			memset( sendmessage, 0, MAX_LINE_LEN);
			sprintf(sendmessage,"data_number %d\n",f+1);
			sprintf(sendmessage,"%sId    : %d\n",sendmessage,profile_data_store[f].id);
			sprintf(sendmessage,"%sName  : %s\n",sendmessage,profile_data_store[f].name);
			sprintf(sendmessage,"%sBirth : %04d-%02d-%02d\n",sendmessage,profile_data_store[f].birthday.year,
				profile_data_store[f].birthday.month,profile_data_store[f].birthday.day);
			sprintf(sendmessage,"%sAddr. : %s\n",sendmessage,profile_data_store[f].address);
			sprintf(sendmessage,"%sComm. : %s\n\n",sendmessage,profile_data_store[f].other);
			
			Send_Server2client( socket, sendmessage);
		}else{/*もしあてはあるものなかったらmissMatchDataに1を追加する*/
			missMatchData++;
		}
	}
	
	memset( sendmessage, 0, MAX_LINE_LEN);
	sprintf(sendmessage,"%s",FinishMessage);
	Send_Server2client(socket, sendmessage);
	printf("%%Fコマンドで%sを検索しました．\n",word);
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
void cmd_sort(int socket, int order){
	char str[MAX_LINE_LEN]; 
	
	if(1<=order && order<=5){
		quick_sort(0,profile_data_nitems-1,order);
		printf("要素 %d でソートが完了しました\n",order);
		memset( str, 0, MAX_LINE_LEN);
		sprintf(str,"要素 %d でソートが完了しました\n",order);
		Send_Server2client(socket, str);
		if(profile_data_nitems == MAX_PROFILES && IsOverwriteMode == 1){	/*保存数が10000件の時にソートを行ったら上書きの場所を先頭に戻す*/
			profile_data_changeIndex = 0;
		}
	}else{
		fprintf(stderr,"あなたが入力した数=%dではソートできません．1から5の数を入力してください．\n",order);
		memset( str, 0, MAX_LINE_LEN);
		sprintf(str,"あなたが入力した数=%dではソートできません．1から5の数を入力してください．\n",order);
		Send_Server2client(socket,str);
	}
}

/*----------------------------------------------------------------------------*/
/*上書きモードON(1),OFF(0)を変更する関数*/
void cmd_overwrite(int socket){
	char str[MAX_LINE_LEN];
	
	if(IsOverwriteMode == 0){
		printf("%%Oを実行しました．\n%d件のデータを保存した場合，それ以降の新規データは先頭に保存されます．\n",MAX_PROFILES);
		memset( str, 0, MAX_LINE_LEN);
		sprintf(str, "%%Oを実行しました．\n%d件のデータを保存した場合，それ以降の新規データは先頭に保存されます．\n",MAX_PROFILES);
		Send_Server2client(socket,str);
		IsOverwriteMode = 1;
		if(profile_data_nitems < MAX_PROFILES){
			profile_data_changeIndex = profile_data_nitems;
		}else if(profile_data_nitems == MAX_PROFILES){
			profile_data_changeIndex = 0;
		}
	}else if(IsOverwriteMode == 1){
		printf("%%Oを実行しました．\nデータの上書きをせずに%d件を超えるとデータを保存しません．\n",MAX_PROFILES);
		memset( str, 0, MAX_LINE_LEN);
		sprintf(str,"%%Oを実行しました．\nデータの上書きをせずに%d件を超えるとデータを保存しません．\n",MAX_PROFILES);
		Send_Server2client(socket,str);
		IsOverwriteMode = 0;
		StopAddDataFlag = 0; /*MAX_PROFILES件を超えたときに出るメッセージをもう一度出るようにする*/
	}
}

/*----------------------------------------------------------------------------*/
void cmd_authority(int socket){
	char str[MAX_LINE_LEN];
	
	if(AuthorityLevel == 0){
		printf("%%Aを実行しました．\n実行権限が低いのでサーバ側にファイル書き込みできません．\n");
		memset( str, 0, MAX_LINE_LEN);
		sprintf(str,"%%Aを実行しました．\n実行権限が低いのでサーバ側にファイル書き込みできません．\n");
		Send_Server2client(socket,str);
	}else if(AuthorityLevel == 1){
		if(IsServerPreserveData == 0 && IsCmdRServerFile == 0){
			printf("%%Aを実行しました．\nサーバ側にファイル書き込みします．\n");
			memset( str, 0, MAX_LINE_LEN);
			sprintf(str,"%%Aを実行しました．\nサーバ側にファイル書き込みします．\n");
			Send_Server2client(socket,str);
			IsServerPreserveData = 1;
			IsCmdRServerFile = 1;
		}else if(IsServerPreserveData == 1 && IsCmdRServerFile == 1){
			printf("%%Aを実行しました．\nクライアント側にファイル書き込みします．\n");
			memset( str, 0, MAX_LINE_LEN);
			sprintf(str,"%%Aを実行しました．\nクライアント側にファイル書き込みします．\n");
			Send_Server2client(socket,str);
			IsServerPreserveData = 0;
			IsCmdRServerFile = 0;
		}
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
	%A：<%A>         権限変更，管理者のみ使用可能
	*/
void exec_command(int socket, char cmd, char *param){
	char str[MAX_LINE_LEN];
	
	switch (cmd) {
	case 'Q': cmd_quit(socket); break;
	case 'C': cmd_check(socket); break;
	case 'P':{
			if(('0'<=param[0]&&param[0]<='9')||(param[0]=='-' && '0'<=param[1]&&param[1]<='9') ){
				cmd_print(socket,atoi(param));
			}else{
				printf("数字を入力してください．\n");
				memset( str, 0, MAX_LINE_LEN);
				sprintf(str,"数字を入力してください．\n");
				Send_Server2client(socket,str);
			}
			break;
		}
	case 'R': cmd_read(socket, param);break;
	case 'W': cmd_write(socket, param); break;
	case 'F': cmd_find(socket, param); break;
	case 'S': cmd_sort(socket, atoi(param)); break;
	case 'O': cmd_overwrite(socket); break;
	case 'A': cmd_authority(socket); break;
	default:
		fprintf(stderr,"Invalid command %c: ignored.\n\n",cmd);
		memset( str, 0, MAX_LINE_LEN);
		sprintf(str,"Invalid command %c: ignored.\n\n",cmd);
		Send_Server2client(socket,str);
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
struct profile *new_profile(int socket, struct profile *p,char *csv){
	char *ptr[5];
	char sendmessage[MAX_LINE_LEN];
	
	if(split(csv, ptr, ',', 5) != 5){
		if(IsOverwriteMode==0){	/*要素が5つないときに保存場所を使用するのを防ぐ*/
			profile_data_nitems = profile_data_nitems - 1;
		}else if(IsOverwriteMode==1){
			profile_data_changeIndex = profile_data_changeIndex - 1;
		}
		
		fprintf(stderr, "your data is not five factors．\n");
		if(IsStartCmdR == 0){
			memset( sendmessage, 0, MAX_LINE_LEN);
			sprintf(sendmessage, "your data is not five factors．\n");
			Send_Server2client(socket,sendmessage);
		}
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
	
	if(IsStartCmdR == 0){
		memset( sendmessage, 0, MAX_LINE_LEN);
		sprintf(sendmessage, "Your Input Data was registered\n");
		Send_Server2client(socket,sendmessage);
	}
	
	return p;
}

/*----------------------------------------------------------------------------*/
	/*
	コマンドなのか文字列なのかを識別し，処理を他の関数に移行する処理を行う関数
	<上書きモード>
	MAX_PROFILESを超えるまでは，通常モードと同じようにデータを追加
	超えると，先頭から追加データを保存するようになる
	*/
void parse_line(int socket, char *line){
	char str[MAX_LINE_LEN];
	if (line[0] == '%'&& line[2] != ' ' && line[1] != 'Q' && line[1] != 'C'&&line[1]!='O' && line[1] != 'A') {
		if(line[1]=='P'|| line[1]=='F'|| line[1]=='R' ||line[1]=='W'|| line[1]=='S'){	/*コマンドで追加データを使用するものの空白がないことを通知*/
			fprintf(stderr,"Your input command%%%c Not blank．line[2]=%c\n",line[1],line[2]);
			memset( str, 0, MAX_LINE_LEN);
			sprintf(str,"Your input command%%%c Not blank．line[2]=%c\n",line[1],line[2]);
			Send_Server2client(socket,str);
		}else{
			exec_command(socket ,line[1],&line[3]);
		}
	}else if(line[0] == '%'){
		exec_command(socket,line[1],&line[3]);
	}else{
		if(IsOverwriteMode == 0){
			if(profile_data_nitems != MAX_PROFILES){	/*データの保存数が10000件を超えたときに保存を中止するようにするための条件文*/
				new_profile(socket,&profile_data_store[profile_data_nitems++], line);
			}else if(StopAddDataFlag==0){
				printf("%d件のデータが保存されています．新しく保存する場合は上書きモードにコマンド%%Oで変更してください．\n",MAX_PROFILES);
				
				StopAddDataFlag = 1;
			}else if(IsStartCmdR == 0){
				printf("%d件保存されています．追加したい場合は上書きモードに変えてください!\n",profile_data_nitems);
				memset( str, 0, MAX_LINE_LEN);
				sprintf(str,"%d件保存されています．追加したい場合は上書きモードに変えてください!\n",profile_data_nitems);
				Send_Server2client(socket,str);
			}
		}else if(IsOverwriteMode == 1){
			if(profile_data_changeIndex < MAX_PROFILES){	/*上書き場所によって書き込む場所を変更するかを判断*/
				if(profile_data_nitems != MAX_PROFILES){	/*データを10000件未満の場合は追加保存する前に10000件までデータを保存させる*/
					new_profile(socket,&profile_data_store[profile_data_changeIndex++], line);
					profile_data_nitems++;	/*上書きモード終了後では，profile_data_nitems使用するので数字を1追加しておく*/
				}else if(profile_data_nitems==MAX_PROFILES){
					new_profile(socket,&profile_data_store[profile_data_changeIndex++], line);
				}
			}else if(profile_data_changeIndex==MAX_PROFILES){	/*上書き場所の更新*/
				profile_data_changeIndex = 0;
				new_profile(socket,&profile_data_store[profile_data_changeIndex++], line);
			}
		}
	}
}
/*----------------------------------------------------------------------------*/