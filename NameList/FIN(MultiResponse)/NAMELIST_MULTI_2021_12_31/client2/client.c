/*library------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

/*define-----------------------------------------------------*/
#define MAX_LINE_LEN 2048
#define PORT "54321"

/*global-----------------------------------------------------*/
char FinishMessage[] = "FINISH";
char ErrorRead[] = "Error:Read";
char ErrorArg[] = "Error:argument\n";
char ErrorGetaddrinfo[] = "Error:getaddrinfo\n";
char ErrorConnect[] = "Error:connect\n";
char ErrorSend[] = "Error:send\n";
char ErrorRecv[] = "Error:recv\n";
char ErrorFile[] = "Error:file\n";
char InputMessage[] = "\n%%-------INPUT-----------------------------------------------%%\n";
char OutputMessage[] = "\n%%-------OUTPUT----------------------------------------------%%\n";

int JudgeAuthority = 0;
int authorityLevel = 0;
int IsWriteClient = 1;
int IsReadClient = 1;

/*prototype declare------------------------------------------*/
int Get_Line(FILE *fp, char *line);
int Subst(char *str, char c1, char c2);
int Char_Num_Count(char string[]);
void Input_Message();
void Output_Message();
void Data_Recv_Cliant(int socket);
void Authority_Level(int socket, int judgeAuthority, char *cmdlineArg);
int Communication_Server(int socket);
void Cmd_P_Output(int socket);
void Cmd_R_Clientfile(int socket, char *filename);
void Cmd_W_Write_Client(int socket, char *filename);
void Cmd_F_Output(int socket);

/*main-------------------------------------------------------*/
int main(int argc, char const *argv[]){
	struct addrinfo hints;
	struct addrinfo *res;
	struct in_addr addr;
	char *sendmessage;
	int clientSocket;
	int strNum;
	
	//コマンドライン引数の個数で処理を分岐
	if(argc == 1){
		write(2, ErrorArg, Char_Num_Count(ErrorArg));
	}else if(argc == 3){
		JudgeAuthority = 1;
	}else{
		JudgeAuthority = 0;
	}
	
	//①ドメイン名からIPアドレスを確認：getaddrinfo
	memset(&hints, 0 ,sizeof(struct addrinfo));
	hints.ai_family = AF_INET; //IPv4:AF_INET
	hints.ai_socktype = SOCK_STREAM; //TCPに設定
	int ret = getaddrinfo(argv[1], PORT , &hints, &res);
	if(ret != 0){
		write(2, ErrorGetaddrinfo, Char_Num_Count(ErrorGetaddrinfo));
	}
	
	//IPアドレスを確認
	//printf("%u\n",((struct sockaddr_in *)(res->ai_addr))->sin_addr.s_addr);
	addr.s_addr = ((struct sockaddr_in *)(res->ai_addr))->sin_addr.s_addr;
	write(1,inet_ntoa(addr),Char_Num_Count(inet_ntoa(addr)) );
	write(1, "\n", 1);
	
	//②socket
	clientSocket = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	
	//③connect
	if( (strNum = connect(clientSocket, res->ai_addr, res->ai_addrlen)) == -1){
		write(2,ErrorConnect,Char_Num_Count(ErrorConnect));
	}
	
	//権限確認
	sendmessage = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
	memset(sendmessage , 0, MAX_LINE_LEN);
	if(JudgeAuthority == 1){
		sprintf(sendmessage,"%s",argv[2]);
		Authority_Level(clientSocket, JudgeAuthority, sendmessage);
	}else if(JudgeAuthority == 0){
		sprintf(sendmessage,"My Normal User");
		Authority_Level(clientSocket, JudgeAuthority, sendmessage);
	}
	free(sendmessage);
	
	//④サーバとの通信の処理⑤send⑥recv
	Communication_Server(clientSocket);
	
	//⑦ソケットを削除
	close(clientSocket);
}

/*function---------------------------------------------------*/
/*-----------------------------------------------------------*/
int Char_Num_Count(char string[]){
	int i=0;
	for(i=0; string[i] != '\0'; i++){;}
	
	return i;
}

/*-----------------------------------------------------------*/
	/*
	Subst関数
	*str：文字列
	c1：変更したい文字
	c2：変更する文字
	*/
int Subst(char *str, char c1, char c2){
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

int Get_Line(FILE *fp, char *line){
		/*fgetsで一行の入力MAX_LINELEN行プラス改行文字のMAX_LINE_LEN+1文字と制限して行う．実行できたら，
			elseの方に移りSubst関数でエンターキーでの改行文字を終端文字に変換する．*/
	if(fgets(line, MAX_LINE_LEN + 1, fp) == NULL){
		return 0;
	}else{
		Subst(line, '\n', '\0');
		return 1;
	}
}

/*-----------------------------------------------------------*/
void Input_Message(){
	write(1,InputMessage ,Char_Num_Count(InputMessage));
}

/*-----------------------------------------------------------*/
void Output_Message(){
	write(1,OutputMessage ,Char_Num_Count(OutputMessage));
}

/*-----------------------------------------------------------*/
/*
相手からのデータを受け取る関数
受け取ったものを出力する
*/
void Data_Recv_Cliant(int socket){
	char *receivebuffer;
	int strNum;
	
	receivebuffer = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
	memset(receivebuffer, 0, MAX_LINE_LEN);
	if( ((strNum = recv(socket, receivebuffer, MAX_LINE_LEN, 0)) == -1)){
		write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
	}
	write(1, receivebuffer, strNum);
	free(receivebuffer);
}

/*-----------------------------------------------------------*/
/*
サーバに権限変更を要請
*/
void Authority_Level(int socket, int judgeAuthority, char *sendmessage){
	char *receivebuffer;
	int strNum;
	
	if(judgeAuthority == 1){
		if( (strNum = send(socket,sendmessage,Char_Num_Count(sendmessage), 0) ) == -1){
			write(2,ErrorSend,Char_Num_Count(ErrorSend));
		}
	}else if(judgeAuthority == 0){
		if( (strNum = send(socket,sendmessage,Char_Num_Count(sendmessage), 0) ) == -1){
			write(2,ErrorSend,Char_Num_Count(ErrorSend));
		}
	}
	
	receivebuffer = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
	memset(receivebuffer, 0, MAX_LINE_LEN);
	if( ((strNum = recv(socket, receivebuffer, MAX_LINE_LEN, 0)) == -1)){
		write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
	}
	
	if(strcmp( receivebuffer,"YOUR ADMINISTRATOR" )== 0){
		authorityLevel = 1;
		write(1, receivebuffer, strNum);
		printf("\n%%W,%%Rは始めクライアント側のファイル操作です．\n%%Aコマンドでサーバ側に変更できます!\n");
	}else{
		authorityLevel = 0;
		write(1, receivebuffer, strNum);
		printf("\n%%W,%%Rはクライアント側のファイル操作のみです．\n");
	}
	
	free(receivebuffer);
}

/*-----------------------------------------------------------*/
int Communication_Server(int socket){
	char sendbuffer[MAX_LINE_LEN];
	int strNum;
	
	while(1){
		//標準入力待ち read
		Input_Message();
		memset( sendbuffer , 0, MAX_LINE_LEN);
		if( (strNum = read(0, sendbuffer, MAX_LINE_LEN ) )  == -1){
			write(2,ErrorRead,Char_Num_Count(ErrorRead));
		}
		
		//④send
		if( (strNum = send(socket,sendbuffer,MAX_LINE_LEN , 0) ) == -1){
			write(2,ErrorSend,Char_Num_Count(ErrorSend));
		}
		
		//⑤名簿管理でコマンドごとにどのような処理を待つか．
		if(sendbuffer[0] != '%'){
			Output_Message();
			Data_Recv_Cliant(socket);
		}else if(sendbuffer[0] == '%'){
			switch(sendbuffer[1]){
				case 'Q' :{ Output_Message(); Data_Recv_Cliant(socket); return 0; break;}
				case 'C' :{ Output_Message(); Data_Recv_Cliant(socket); break;}
				case 'P' :{ 
					if(sendbuffer[2] == ' ' && (sendbuffer[3]=='-' || ('0'<=sendbuffer[3]&& sendbuffer[3]<='9') ) ){
						Cmd_P_Output(socket); 
					}else{
						Output_Message(); Data_Recv_Cliant(socket);
					}
					break;
				}
				case 'R' :{ 
					if(IsReadClient == 1){
						Cmd_R_Clientfile(socket , &sendbuffer[3]);
					}else if(IsReadClient == 0){
						Output_Message(); Data_Recv_Cliant(socket);
					}
					break;
				}
				case 'W' :{ 
					if(IsWriteClient == 0){
						Output_Message(); Data_Recv_Cliant(socket);
					}else if(IsWriteClient == 1){
						Cmd_W_Write_Client(socket, &sendbuffer[3]);
					}
					break;
				}
				case 'S' :{ Output_Message(); Data_Recv_Cliant(socket); break;}
				case 'F' :{ Cmd_F_Output(socket); break;}
				case 'O' :{ Output_Message(); Data_Recv_Cliant(socket); break;}
				case 'A' :{ 
					if(authorityLevel== 1 ){
						if(IsWriteClient == 0 && IsReadClient == 0){
							IsWriteClient = 1; IsReadClient = 1;
						}else if(IsWriteClient == 1 && IsReadClient == 1){;
							IsWriteClient = 0; IsReadClient = 0;
						}
					}
					Output_Message(); Data_Recv_Cliant(socket); break;
				}
				default  :{ Output_Message(); Data_Recv_Cliant(socket); break;}
			}
		}
		
		memset( sendbuffer , 0, MAX_LINE_LEN);
	}
	return 0;
}

/*-----------------------------------------------------------*/
/*
%Pの処理を一つデータごとに送るための処理
*/
void Cmd_P_Output(int socket){
	int strSize;
	char *recvData;
	
	Output_Message();
	
	while(1){
		recvData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
		memset(recvData, 0, MAX_LINE_LEN);
		if( ((strSize = recv(socket, recvData, MAX_LINE_LEN, 0)) == -1)){
			write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
		}
		
		if(strcmp(recvData, FinishMessage) == 0){
			break;
		}else{
			write(1, recvData, MAX_LINE_LEN);
		}
		free(recvData);
	}
}

/*-----------------------------------------------------------*/
/*
コマンド%W時の，クライアント側で書き込む場合に使用
*/
void Cmd_W_Write_Client(int socket, char *filename){
	int strSize;
	char *recvData;
	
	//書き込みファイルの準備
	strSize = Char_Num_Count(filename);
	filename[strSize-1] = '\0';
	int file_fd = open(filename, O_RDWR | O_CREAT | O_APPEND, S_IRWXU | S_IRWXO);
	
	Output_Message();
	
	while(1){
		recvData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
		memset(recvData, 0, MAX_LINE_LEN);
		if( ((strSize = recv(socket, recvData, MAX_LINE_LEN, 0)) == -1)){
			write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
		}
		//終了判定
		if(strcmp(recvData, FinishMessage) == 0){
			break;
		}else{
			write(file_fd, recvData, strSize);
		}
		free(recvData);
	}
}

/*-----------------------------------------------------------*/
//cmd_F用関数
void Cmd_F_Output(int socket){
	int strSize;
	char *recvData;
	
	Output_Message();
	
	while(1){
		recvData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
		memset(recvData, 0, MAX_LINE_LEN);
		if( ((strSize = recv(socket, recvData, MAX_LINE_LEN, 0)) == -1)){
			write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
		}
		
		if(strcmp(recvData,FinishMessage) == 0){
			break;
		}else{
			write(1, recvData, strSize);
		}
		free(recvData);
	}
}

/*-----------------------------------------------------------*/
void Cmd_R_Clientfile(int socket, char *filename){
	FILE *fp;
	char length[MAX_LINE_LEN];
	int filenameLen;
	int sendSize, recvSize;
	char *sendData, *recvData;
	int readLineCount=0;
	
	//書き込みファイルの準備
	filenameLen = Char_Num_Count(filename);
	filename[filenameLen-1] = '\0';
	fp = fopen(filename, "r");
	
	Output_Message();
	
	if(fp == NULL){
		fprintf(stderr,"%%R: file open error.\n\n");
		sendData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
		memset(sendData, 0, MAX_LINE_LEN);
		sprintf(sendData,"%s",FinishMessage);
		if( ((sendSize = send(socket, sendData, MAX_LINE_LEN, 0)) == -1)){
			write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
		}
		free(sendData);
		
		recvData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
		memset(recvData, 0, MAX_LINE_LEN);
		if( ((recvSize = recv(socket, recvData, MAX_LINE_LEN, 0)) == -1)){
			write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
		}
		write(1,recvData,MAX_LINE_LEN);
		free(recvData);
	}else{
		printf("%sを送信しました．\n",filename);
		while(Get_Line(fp, length) != 0){
			
			sendData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
			memset( sendData , 0, MAX_LINE_LEN);
			sprintf(sendData,"%s",length);
			if((sendSize = send(socket, sendData ,MAX_LINE_LEN, 0) ) == -1){
				write(2,ErrorSend,Char_Num_Count(ErrorSend));
			}
			free(sendData);
			readLineCount++;
		}
		sendData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
		memset(sendData, 0, MAX_LINE_LEN);
		sprintf(sendData,"%s",FinishMessage);
		if( ((sendSize = send(socket, sendData, MAX_LINE_LEN, 0)) == -1)){
			write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
		}
		free(sendData);
		if(readLineCount == 0){
			recvData = (char*)malloc( (MAX_LINE_LEN) * sizeof(char));
			memset(recvData, 0, MAX_LINE_LEN);
			if( ((recvSize = recv(socket, recvData, MAX_LINE_LEN, 0)) == -1)){
				write(2,ErrorRecv,Char_Num_Count(ErrorRecv));
			}
			free(recvData);
		}
	}
}
/*-----------------------------------------------------------*/