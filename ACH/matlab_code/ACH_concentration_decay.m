function ACH = ACH_concentration_decay(data, input_options)
% A function computes air change per hour(ACH) with given concentration
% decay measurement data
%
%   inputs
%       - data input: time
%       - data input: concentration
%       - options
%
%   outputs
%       - figure
%       - min/max (or 95% confidence interval) of ACH
%
%   equation?
%
% modify options

if length(data.time) ~= length(data.c)
    error('Time and concentration data should have consistent length')
end

% options

input_options

if(exist('input_options','var') && ~isempty(input_options))
    display('1asdasd')
    if(~exist('input_options.minute_average','var'))   
        display('minute average option not exist');
        input_options.minute_average = false; 
    end
    if(~exist('input_options.smoothing_scheme')) input_options.smoothing_scheme = 'moving'; end
    if(~exist('input_options.smoothing_span'))   input_options.smoothing_span = 31; end
    if(~exist('input_options.plot'))             input_options.plot = true; end
else
    input_options.minute_average = false;
    input_options.smoothing_scheme = 'moving';
    input_options.smoothing_span = 31;
    input_options.plot = true;
end

input_options


TT_raw = timetable(data.time, data.c);

if input_options.minute_average
    TT = retime(TT_raw,'minutely','mean');
    TT.c = TT.Var1;
    time_scale = 60;
else
    TT = TT_raw;
    TT.c = smooth(TT_raw.Var1,input_options.smoothing_span,input_options.smoothing_scheme);
    time_scale = 1;
end


% index of peak concentration
idx_peak = find(max(TT.c) == TT.c);


c_peak  = min(TT.c(idx_peak));
c_exp   = TT.c(idx_peak+1:end);
del_t   = 1:length(c_exp);


ACH = -log(c_exp/c_peak)./del_t'*3600/time_scale;

if input_options.plot
    figure();
    subplot(1,2,1);hold on
    plot(TT_raw.Time,TT_raw.Var1,'color',[0.5 0.5 1.0])
    plot(TT.Time,TT.c,'k','linewidth',2);
    legend('Raw data','Smoothed data')
    legend boxoff
    xlabel('Time'); ylabel('Tracer concentration');
    
    subplot(1,2,2);
    plot(del_t*time_scale/60, ACH, 'b','linewidth',2);
    xlabel('Time [min]'); ylabel('ACH [1/h]');
end


end
