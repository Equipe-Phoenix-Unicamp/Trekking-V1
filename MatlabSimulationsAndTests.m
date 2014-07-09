clear all; close all; clc;

time = 1:0.001:5;
entrada(1:length(time)) = 1;
timez1 = 1:0.1:5;
entradaz1(1:length(timez1)) = 1;
timez2 = 1:0.05:5;
entradaz2(1:length(timez2)) = 1;


s = tf('s');
pole0 = -0.03;
pole1 = -130;
gain = 120;

sis = gain/((1-s/pole0)*(1-s/pole1))/s;

%sisotool(sis)

cont = 3.0438*(1+1.3*s)*(1+0.97*s)/s;

sisC = feedback(sis*cont,1);

stcontinuo = lsim(sisC,entrada,time);


t1 = 0.1;
sisz1 = c2d(sis, t1, 'zoh');
contz1 = c2d(cont, t1, 'tustin');
sisCz1 = feedback(sisz1*contz1,1);
stz1=lsim(sisCz1,entradaz1,timez1);


t2 = 0.05;
sisz2 = c2d(sis, t2, 'zoh');
contz2 = c2d(cont, t2, 'tustin');
sisCz2 = feedback(sisz2*contz2,1);
stz2=lsim(sisCz2,entradaz2,timez2);


figure, plot(timez1,stz1,timez2,stz2,time,stcontinuo), legend('discreto1','discreto2','continuo');